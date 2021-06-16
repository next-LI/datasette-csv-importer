from urllib.parse import quote_plus
import asyncio
import datetime
import io
import json
import os
import sqlite3
import sqlite_utils
import sys
import time
import tempfile
import uuid

from csvs_to_sqlite.cli import cli as command
from datasette import hookimpl
from datasette.database import Database
from datasette.utils.asgi import Response, Forbidden
from starlette.requests import Request

from .git_utils import save_folder_to_repo


DEFAULT_STATUS_TABLE="_csv_importer_progress_"
DEFAULT_DBPATH="."
DEFAULT_CSVSPATH="./csvs"
DEFAULT_LIVE_METADATA=False
DEFAULT_USE_LIVE_PERMISSIONS=True


def get_dbpath(plugin_config):
    """
    Get the path where to build SQlite databases. Default: .
    """
    return plugin_config.get("database_path", DEFAULT_DBPATH)


def get_use_live_permissions(plugin_config):
    """
    Whether or not to use the __metadata table as supported
    by the next-LI/datasette_live_config plugin.
    """
    return plugin_config.get(
        "use_live_permissions", DEFAULT_USE_LIVE_PERMISSIONS
    )


def get_use_live_metadata(plugin_config):
    """
    Whether or not to use the __metadata table as supported
    by the next-LI/datasette_live_config plugin.
    """
    return plugin_config.get("use_db_metadata", DEFAULT_LIVE_METADATA)


def get_csvspath(plugin_config):
    """
    Get the path where to save the uploaded CSV files and import config.
    Default: ./csvs
    """
    return plugin_config.get("csvs_path", DEFAULT_CSVSPATH)


def get_status_table(plugin_config):
    return plugin_config.get("status_table", DEFAULT_STATUS_TABLE)


def get_status_database(datasette, plugin_config):
    """
    Get a database, based on the `database` plugin setting (or the first
    mutable DB in the list of databases) to read from.
    """
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
    try:
        return datasette.databases[database]
    except KeyError:
        pass
    database_path = os.path.join(DEFAULT_DBPATH, f"{database}.db")
    sqlite3.connect(database_path)
    datasette.add_database(
        Database(datasette, path=database_path, is_mutable=True),
        name=database,
    )
    return datasette.databases[database]


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


async def csv_importer_status(scope, receive, datasette, request):
    if not await datasette.permission_allowed(
        request.actor, "csv-importer", default=False
    ):
        raise Forbidden("Permission denied for csv-importer")

    plugin_config = datasette.plugin_config(
        "datasette-csv-importer"
    ) or {}

    db = get_status_database(datasette, plugin_config)
    status_table = get_status_table(plugin_config)

    query = f"select * from {status_table} where id = ? limit 1"
    result = await db.execute(query, (request.url_vars["task_id"],))
    run = result.first()
    return Response.json(run)


def set_perms_for_live_permissions(datasette, actor, db_name):
    # TODO: pull from live-config plugin config to get db path
    # add the permission table, grant access to current user only
    # this will create the DB if not exists
    if not os.path.exists("live_permissions.db"):
        return

    if not actor:
        return

    db = sqlite_utils.Database(sqlite3.connect("live_permissions.db"))

    group_name = f"DB Access: {db_name}"
    db["groups"].insert({
        "name": group_name,
    }, pk="id", replace=True)

    group_id = None
    for row in db["groups"].rows_where('name=?', (group_name,)):
        group_id = row["id"]
        break

    print("Group ID", group_id)

    group_action_resources = [{
        "action": "view-database",
        "resource_primary": db_name,
    }, {
        "action": "view-table",
        "resource_primary": db_name,
    }, {
        "action": "live-config",
        "resource_primary": db_name,
    }]
    for ar_data in group_action_resources:
        print("Adding A/R:", ar_data)
        db["actions_resources"].insert(ar_data, pk="id", replace=True)
        query = 'action=:action and resource_primary=:resource_primary'
        args = tuple(ar_data.values())
        ar_id = None
        for row in db["actions_resources"].rows_where(query, args):
            ar_id = row["id"]
            break
        print("A/R ID", ar_id)
        db["permissions"].insert({
            "group_id": group_id,
            "actions_resources_id": ar_id
        }, pk="id", alter=False, replace=True)

    # find user
    user_id = None
    for key, value in actor.items():
        if not value:
            continue
        if not isinstance(value, str) and not isinstance(value, int):
            continue
        query = "lookup=? and value=?"
        args = (f"actor.{key}", value)
        for row in db["users"].rows_where(query, args):
            user_id = row["id"]
            break

    print("Found User ID", user_id)

    # add user to group
    db["group_membership"].insert({
        "user_id": user_id,
        "group_id": group_id,
    }, pk=("group_id", "user_id"), replace=False, ignore=True)


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

    plugin_config = datasette.plugin_config(
        "datasette-csv-importer"
    ) or {}
    print("plugin_config", plugin_config)

    db = get_status_database(datasette, plugin_config)
    status_table = get_status_table(plugin_config)

    # We need the ds_request to pass to render_template for CSRF tokens
    ds_request = request

    # We use the Starlette request object to handle file uploads
    starlette_request = Request(scope, receive)
    # If we aren't uploading a new file (POST), show uploader screen
    if starlette_request.method != "POST":
        print("plugin_config", plugin_config)
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

    outfile_db = os.path.join(get_dbpath(plugin_config), f"{basename}.db")

    if basename in datasette.databases:
        if not await datasette.permission_allowed(
            request.actor, "view-database", (basename,), default=False
        ):
            raise Forbidden("view-database access required for existing database!")

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
    await db.execute_write_fn(insert_initial_record, block=True)

    args = []
    for key, value in formdata.items():
        if not key.startswith("-"):
            continue
        if key in ["-t", "--table"]:
            csv_table_name = value
        # this is a toggle/flag arg with no param
        if value is True or value == "true":
            args.append(key)
            continue
        if not value or value == "false":
            continue
        args.append(key)
        args.append(value)

    def set_status(status_database, message):
        status_database[status_table].update(
            task_id,
            {
                "message": message,
            },
        )

    # run the command, capture its output
    def run_cli_import(conn):
        status_database = sqlite_utils.Database(conn)
        set_status(status_database, "Running CSV import...")

        exitcode = -1
        output = None
        try:
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(csv.file.read())
                temp.flush()

                args.append(temp.name)
                args.append(outfile_db)

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
                    if not os.path.exists(outfile_db) and not exitcode:
                        exitcode = -2
        except Exception as e:
            print("Exception", e)
            exitcode = -2
            message = str(e)

        set_status(status_database, "Adding database to internal DB list...")
        # Adds this DB to the internel DBs list
        if basename not in datasette.databases:
            print("Adding database", basename)
            datasette.add_database(
                Database(datasette, path=outfile_db, is_mutable=True),
                name=basename,
            )
            # print("Database added successfully!")
            # try:
            #     loop = asyncio.get_running_loop()
            # except RuntimeError:
            #     loop = asyncio.new_event_loop()
            # print("Running schema refresh...")
            # loop.run_until_complete(datasette.refresh_schemas())
            # print("Schema refresh complete!")

        csvspath = get_csvspath(plugin_config)
        if csvspath:
            set_status(status_database, "Saving CSV to server directory...")
            csv_db_name = args[-1].replace(".db", "")
            csv_table_name = csv_db_name
            if "-t" in formdata:
                csv_table_name = formdata["-t"]
            if "--table" in formdata:
                csv_table_name = formdata["--table"]
            outfile_csv = os.path.join(
                csvspath, f"{csv_db_name}--{csv_table_name}.csv"
            )
            outfile_args = os.path.join(
                csvspath, f"{csv_db_name}--{csv_table_name}.json"
            )

            # success! save our configs and CSV
            print("Writing CSV", outfile_csv)
            with open(outfile_csv, "wb") as f:
                csv.file.seek(0)
                f.write(csv.file.read())

            print("Writing args to", outfile_args)
            with open(outfile_args, "w") as f:
                f.write(json.dumps(args, indent=2))

        if get_use_live_metadata(plugin_config):
            set_status(status_database, "Running live-config plugin integration...")
            # add the permission table, grant access to current user only
            # this will create the DB if not exists
            db = sqlite_utils.Database(sqlite3.connect(outfile_db))
            try:
                db["__metadata"].get("allow")
            except sqlite_utils.db.NotFoundError:
                # don't overwrite, only create
                db["__metadata"].insert({
                    "key": "tables",
                    "value": json.dumps({
                        "__metadata": {
                            "hidden": True
                        }
                    }),
                }, pk="key", alter=True, replace=False, ignore=True)

        if get_use_live_permissions(plugin_config):
            set_status(status_database, "Running live-permissions plugin integration...")
            set_perms_for_live_permissions(datasette, request.actor, basename)

        # Make a commit
        repo_owner = plugin_config.get("repo_owner")
        repo_name = plugin_config.get("repo_name")
        github_user = plugin_config.get("github_user")
        github_token = plugin_config.get("github_token")
        if csvspath and repo_owner and repo_name and github_user and github_token:
            set_status(status_database, "Saving CSV to git repository...")
            print("Writing csv to repo", filename, csv.file)
            git_output = None
            with Capturing() as git_output:
                try:
                    head_sha = save_folder_to_repo(
                        folder_path=csvspath,
                        repo_owner=repo_owner,
                        repo_name=repo_name,
                        github_user=github_user,
                        github_token=github_token,
                    )
                    print(f"CSV successfully saved!")
                    print(f"HEAD SHA: {head_sha}")
                except Exception as e:
                    print(f"Error saving using git: {e}")

            output = git_output + output

        message = "Import successful!" if not exitcode else "Failure"
        print("Updating status", message)
        status_database[status_table].update(
            task_id,
            {
                "completed": str(datetime.datetime.utcnow()),
                "exitcode": exitcode,
                "status": "completed",
                "message": message,
                "output": "\n".join(output),
            },
        )

    await db.execute_write_fn(run_cli_import)

    if formdata.get("xhr"):
        return Response.json(
            {
                "url": "/{filename}".format(
                    filename=quote_plus(filename),
                ),
                "status_database_path": quote_plus(db.name),
                "status_table": quote_plus(status_table),
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
