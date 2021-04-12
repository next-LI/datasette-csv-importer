from datasette import hookimpl
from datasette.database import Database
from datasette.utils.asgi import Response, Forbidden
from starlette.requests import Request
from urllib.parse import quote_plus
import asyncio
import datetime
import io
import os
import sqlite_utils
import sys
import tempfile
import uuid

from csvs_to_sqlite.cli import cli as command


DEFAULT_STATUS_TABLE="_csv_importer_progress_"
DEFAULT_DBPATH="."


@hookimpl
def permission_allowed(actor, action):
    if action == "csv-importer" and actor and actor.get("id") == "root":
        return True


@hookimpl
def register_routes():
    return [
        (r"^/-/csv-importer$", csv_importer),
        (r"^/-/csv-importer/(?P<task_id>.*)$", csv_importer_status),
    ]


@hookimpl
def menu_links(datasette, actor):
    async def inner():
        allowed = await datasette.permission_allowed(
            actor, "csv-importer", default=False
        )
        if allowed:
            return [{
                "href": datasette.urls.path("/-/csv-importer"),
                "label": "Import CSV"
            }]
    return inner


# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def get_status_table(datasette):
    plugin_config = datasette.plugin_config(
        "datasette-csv-importer"
    ) or {}
    return plugin_config.get("status_table", DEFAULT_STATUS_TABLE)


def get_database(datasette):
    """
    Get a database, based on the `database` plugin setting (or the first
    mutable DB in the list of databases) to read from.
    """
    plugin_config = datasette.plugin_config(
        "datasette-csv-importer"
    ) or {}

    # NOTE: This does not create the DB if it doesn't exist! Use
    # the import endpoint first.
    database = plugin_config.get("status_database")
    if not database:
        # For the moment just use the first database that's not immutable
        database = [
            name
            for name, db in datasette.databases.items()
            if db.is_mutable and not database
        ][0]
    db = datasette.databases[database]
    return db


def get_dbpath(datasette):
    """
    Get the path where to build SQlite databases. Default: .
    """
    plugin_config = datasette.plugin_config(
        "datasette-csv-importer"
    ) or {}
    return plugin_config.get("database_path", DEFAULT_DBPATH)


async def csv_importer_status(scope, receive, datasette, request):
    if not await datasette.permission_allowed(
        request.actor, "csv-importer", default=False
    ):
        raise Forbidden("Permission denied for csv-importer")

    db = get_database(datasette)
    status_table = get_status_table(datasette)

    query = f"select * from {status_table} where id = ? limit 1"
    result = await db.execute(query, (request.url_vars["task_id"],))
    run = result.first()
    return Response.json(run)


async def csv_importer(scope, receive, datasette, request):
    """
    CSV Importer initiates a CSV import using the CLI tool CSVs-to-SQlite.
    Accepts HTTP POST with form data as follows:

    `csv` should contain the CSV file to be imported

    `database` is the name of the database file to be written to. If blank,
    we will choose a name base on the uploaded file name.

    If `xhr` is set to `1` we will assume a JS client is running and this
    endpoint will return JSON (as opposed to rendering a different HTML
    template without `xhr` set to `1`).

    A valid `csrftoken` needs to be provided.

    Any form input starting with "-" are interpreted as arguments to
    the CLI tool. Such arguments are considered single-toggle arguments
    that don't use any parameters, so "--on true" will be interpreted
    as running the tool with "--on".
    """
    if not await datasette.permission_allowed(
        request.actor, "csv-importer", default=False
    ):
        raise Forbidden("Permission denied for csv-importer")

    db = get_database(datasette)
    status_table = get_status_table(datasette)

    # We need the ds_request to pass to render_template for CSRF tokens
    ds_request = request

    # We use the Starlette request object to handle file uploads
    starlette_request = Request(scope, receive)
    # If we aren't uploading a new file (POST), show uploader screen
    if starlette_request.method != "POST":
        return Response.html(
            await datasette.render_template(
                "csv_importer.html", {}, request=ds_request
            )
        )

    formdata = await starlette_request.form()
    csv = formdata["csv"]

    # csv.file is a SpooledTemporaryFile. csv.filename is the filename
    filename = csv.filename
    basename = os.path.splitext(filename)[0]
    if "database" in formdata and formdata["database"]:
        basename = formdata["database"]
    outfile = os.path.join(get_dbpath(datasette), f"{basename}.db")

    task_id = str(uuid.uuid4())

    def insert_initial_record(conn):
        database = sqlite_utils.Database(conn)
        database[status_table].insert(
            {
                "id": task_id,
                "filename": filename,
                "dbname": basename,
                "started": str(datetime.datetime.utcnow()),
                "completed": None,
                "exitcode": -1,
                "status": "in-progress",
                "message": "Setting up import...",
                "output": None,
            },
            pk="id",
            alter=True,
        )
    await db.execute_write_fn(insert_initial_record)

    def import_preparing(conn):
        database = sqlite_utils.Database(conn)
        database[status_table].update(
            task_id,
            {
                "message": "Preparing import options...",
            },
        )
    await db.execute_write_fn(import_preparing)

    args = []
    for key, value in formdata.items():
        if not key.startswith("-"):
            continue
        # this is a toggle/flag arg with no param
        if value is True or value == "true":
            args.append(key)
            continue
        if not value or value == "false":
            continue
        args.append(key)
        args.append(value)

    def set_running(conn):
        database = sqlite_utils.Database(conn)
        database[status_table].update(
            task_id,
            {
                "message": "Running CSV import...",
            },
        )
    await db.execute_write_fn(set_running)

    # run the command, capture its output
    def run_cli_import(conn):
        exitcode = -1
        output = None
        try:
            database = sqlite_utils.Database(conn)

            with tempfile.NamedTemporaryFile() as temp:
                temp.write(csv.file.read())
                temp.flush()

                args.append(temp.name)
                args.append(outfile)

                # run the import command, capturing stdout
                with Capturing() as output:
                    exitcode = command.main(
                        args=args, prog_name="cli", standalone_mode=False
                    )
                    if exitcode is not None:
                        exitcode = int(exitcode)
                    # detect a failure to write DB where tool returns success code
                    # this makes it so we don't have to read the CLI output to
                    # figure out if the command succeeded or not
                    if not os.path.exists(outfile) and not exitcode:
                        exitcode = -2
        except Exception as e:
            exitcode = -2
            message = str(e)

        message = "Import successful!" if not exitcode else "Failure"
        database[status_table].update(
            task_id,
            {
                "completed": str(datetime.datetime.utcnow()),
                "exitcode": exitcode,
                "status": "completed",
                "message": message,
                "output": "\n".join(output),
            },
        )

        if basename not in datasette.databases:
            datasette.add_database(
                Database(datasette, path=outfile, is_mutable=True),
                name=basename,
            )
        loop = asyncio.get_event_loop()
        loop.create_task(datasette.refresh_schemas())

    await db.execute_write_fn(run_cli_import)

    if formdata.get("xhr"):
        return Response.json(
            {
                "url": "/{filename}".format(
                    filename=quote_plus(filename),
                ),
                "status_database_path": quote_plus(db.name),
                "task_id": task_id,
            }
        )

    return Response.html(
        await datasette.render_template(
            "csv_importer_done.html", {
                "filename": filename,
                "task_id": task_id,
            },
        )
    )
