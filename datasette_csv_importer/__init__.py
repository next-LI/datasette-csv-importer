from datasette import hookimpl
from datasette.utils.asgi import Response, Forbidden
from starlette.requests import Request
from urllib.parse import quote_plus
import datetime
import io
import os
import sqlite_utils
import sys
import uuid


from csvs_to_sqlite.cli import cli as command


DEFAULT_PERM=True
STATUS_TABLE="_csv_importer_progress_"


@hookimpl
def permission_allowed(actor, action):
    return True


@hookimpl
def permission_allowed(actor, action):
    if action == "csv-importer" and actor and actor.get("id") == "root":
        return True


@hookimpl
def register_routes():
    return [
        (r"^/-/csv-importer$", csv_importer),
        (r"/-/csv-importer/(?P<task_id>.*)$", csv_importer_status),
    ]


@hookimpl
def menu_links(datasette, actor):
    async def inner():
        allowed = await datasette.permission_allowed(
            actor, "csv-importer", default=DEFAULT_PERM
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


def get_database(datasette):
    """
    Get a database, based on the `database` plugin setting (or the first
    mutable DB in the list of databases) to read from.
    """
    # TODO: pull this from plugin config, using this:
    plugin_config = datasette.plugin_config(
        "datasette-csv-importer"
    ) or {}

    # NOTE: This does not create the DB if it doesn't exist! Use
    # the import endpoint first.
    database = plugin_config.get("database")
    if not database:
        # For the moment just use the first database that's not immutable
        database = [
            name
            for name, db in datasette.databases.items()
            if db.is_mutable and not database
        ][0]
    db = datasette.databases[database]
    return db


async def csv_importer_status(scope, receive, datasette, request):
    if not await datasette.permission_allowed(
        request.actor, "csv-importer", default=DEFAULT_PERM
    ):
        raise Forbidden("Permission denied for csv-importer")

    db = get_database(datasette)
    query = f"select * from {STATUS_TABLE} where id = ? limit 1"
    result = await db.execute(query, (request.url_vars["task_id"],))
    run = result.first()
    return Response.json(run)


async def csv_importer(scope, receive, datasette, request):
    if not await datasette.permission_allowed(
        request.actor, "csv-importer", default=DEFAULT_PERM
    ):
        raise Forbidden("Permission denied for csv-importer")

    db = get_database(datasette)

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
    print("formdata", formdata)
    print("formdata.keys()", formdata.keys())
    print(dir(formdata))
    csv = formdata["csv"]
    # csv.file is a SpooledTemporaryFile. csv.filename is the filename
    filename = csv.filename
    basename = os.path.splitext(filename)[0]

    task_id = str(uuid.uuid4())
    print("Task ID", task_id)

    def insert_initial_record(conn):
        print("Writing initial record", task_id)
        database = sqlite_utils.Database(conn)
        database[STATUS_TABLE].insert(
            {
                "id": task_id,
                "filename": filename,
                "dbname": basename,
                "started": str(datetime.datetime.utcnow()),
                "completed": None,
                "exitcode": -1,
                "status": "in-progress",
                "message": "Beginning import...",
                "output": None,
            },
            pk="id",
            alter=True,
        )

    await db.execute_write_fn(insert_initial_record)
    print("Initial record inserted")

    def run_import(conn):
        print("CSV filename", filename)
        args = ["--help"]
        # args = [*opts, *files, dbpath]
        with Capturing() as output:
            exitcode = command.main(
                args=args, prog_name="cli", standalone_mode=False
            )
            exitcode = int(exitcode)
        message = "Import successful!" if exitcode == 0 else "Failure"
        database = sqlite_utils.Database(conn)
        database[STATUS_TABLE].update(
            task_id,
            {
                "completed": str(datetime.datetime.utcnow()),
                "exitcode": exitcode,
                "status": "completed",
                "message": message,
                "output": "\n".join(output),
            },
        )

    await db.execute_write_fn(run_import)

    if formdata.get("xhr"):
        print("Returning JSON")
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


def get_temporary_file_size(file):
    if isinstance(file._file, (io.BytesIO, io.StringIO)):
        return len(file._file.getvalue())
    try:
        return os.fstat(file._file.fileno()).st_size
    except Exception:
        raise
