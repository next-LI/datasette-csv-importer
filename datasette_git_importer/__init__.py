from datasette import hookimpl
from datasette.utils.asgi import Response, Forbidden
from starlette.requests import Request
from urllib.parse import quote_plus
import csv as csv_std
import codecs
import datetime
import io
import os
import sqlite_utils
import time
import uuid
from .actions_utils import find_run
from .git_utils import write_csv_to_repo


# Environment variables used:
# GITHUB_USER
# GITHUB_TOKEN
# REPO_OWNER
# REPO_NAME
# REPO_DIR


DEFAULT_PERM=True


@hookimpl
def permission_allowed(actor, action):
    if action == "git-importer" and actor and actor.get("id") == "root":
        return True


@hookimpl
def register_routes():
    return [
        (r"^/-/git-importer$", git_importer),
        (r"/-/git-importer/(?P<task_id>.*)$", git_importer_status),
    ]


@hookimpl
def menu_links(datasette, actor):
    async def inner():
        allowed = await datasette.permission_allowed(
            actor, "git-importer", default=DEFAULT_PERM
        )
        if allowed:
            return [{
                "href": datasette.urls.path("/-/git-importer"),
                "label": "Upload and configure CSVs"
            }]

    return inner


async def git_importer_status(scope, receive, datasette, request):
    if not await datasette.permission_allowed(
        request.actor, "git-importer", default=DEFAULT_PERM
    ):
        raise Forbidden("Permission denied for git-importer")

    plugin_config = datasette.plugin_config(
        "datasette-git-importer"
    )
    # leave this here for now to ensure that users deliberately
    # enabled this plugin!
    assert plugin_config, "Error: plugin not configured!"
    assert "github_user" in plugin_config
    assert "github_token" in plugin_config

    task_id = request.url_vars["task_id"]
    print("getting status for task_id", task_id)

    # For the moment just use the first database that's not immutable
    db = [db for db in datasette.databases.values() if db.is_mutable][0]

    query = "select * from _git_import_progress_ where id = ? limit 1"
    result = await db.execute(query, (task_id,))
    print("result", result)
    run = result.first()
    print("run", run)

    head_sha = run["head_sha"]
    print("head_sha", head_sha)

    gh_run = find_run(head_sha, plugin_config)
    print("gh_run", gh_run)

    # TODO: if we have a run_id, save it to the DB, then we
    # can use that to do the lookup next poll

    return Response.json(gh_run)


async def git_importer(scope, receive, datasette, request):
    if not await datasette.permission_allowed(
        request.actor, "git-importer", default=DEFAULT_PERM
    ):
        raise Forbidden("Permission denied for git-importer")

    plugin_config = datasette.plugin_config(
        "datasette-git-importer"
    )
    assert plugin_config, "Error: plugin not configured!"
    assert "repo_owner" in plugin_config
    assert "repo_name" in plugin_config
    assert "github_user" in plugin_config
    assert "github_token" in plugin_config

    # For the moment just use the first database that's not immutable
    db = [db for db in datasette.databases.values() if db.is_mutable][0]

    # We need the ds_request to pass to render_template for CSRF tokens
    ds_request = request

    # We use the Starlette request object to handle file uploads
    starlette_request = Request(scope, receive)
    # If we aren't uploading a new file (POST), show uploader screen
    if starlette_request.method != "POST":
        return Response.html(
            await datasette.render_template(
                "git_importer.html", {}, request=ds_request
            )
        )

    formdata = await starlette_request.form()
    csv = formdata["csv"]
    # csv.file is a SpooledTemporaryFile. csv.filename is the filename
    filename = csv.filename
    if filename.endswith(".csv"):
        filename = filename[:-4]

    print("CSV filename", filename)

    task_id = str(uuid.uuid4())

    def insert_initial_record(conn):
        print("Writing initial record", task_id)
        database = sqlite_utils.Database(conn)
        database["_git_import_progress_"].insert(
            {
                "id": task_id,
                "filename": filename,
                "started": str(datetime.datetime.utcnow()),
                "completed": None,
                "status": None,
                "conclusion": None,
                "head_sha": None,
            },
            pk="id",
            alter=True,
        )

    await db.execute_write_fn(insert_initial_record)
    print("Initial record inserted")

    # def insert_docs(conn):
    #     database = sqlite_utils.Database(conn)
    #     # TODO: Support other encodings:
    #     reader = csv_std.reader(codecs.iterdecode(csv.file, "utf-8"))
    #     headers = next(reader)

    #     docs = (dict(zip(headers, row)) for row in reader)

    #     i = 0

    #     def docs_with_progress():
    #         nonlocal i
    #         for doc in docs:
    #             i += 1
    #             yield doc
    #             if i % 10 == 0:
    #                 database["_csv_progress_"].update(
    #                     task_id,
    #                     {
    #                         "rows_done": i,
    #                         "bytes_done": csv.file.tell(),
    #                     },
    #                 )

    #     database[filename].insert_all(docs_with_progress(), alter=True, batch_size=100)
    #     database["_csv_progress_"].update(
    #         task_id,
    #         {
    #             "rows_done": i,
    #             "bytes_done": total_size,
    #             "completed": str(datetime.datetime.utcnow()),
    #         },
    #     )
    #     return database[filename].count

    # await db.execute_write_fn(insert_docs)

    print("Writing to repo and pushing")

    def updater(**updated_data):
        def update_fn(conn):
            database = sqlite_utils.Database(conn)
            database["_git_import_progress_"].update(
                task_id, updated_data
            )
        return update_fn

    await db.execute_write_fn(updater(status="committing"))

    print("Writing csv to repo", filename, csv.file)
    with csv.file as f:
        head_sha = write_csv_to_repo(
            csv.filename.replace(" ", "_"), f.read(), plugin_config
        )
    print(f"HEAD SHA: {head_sha}")

    if head_sha is None:
        print("No changes detected. Done.")
        await db.execute_write_fn(updater(
            status="completed", conclusion="no changes"
        ))
        return

    await db.execute_write_fn(updater(
        status="commit-pushed", head_sha=head_sha
    ))

    # print("Starting poll for deploy")
    # status = "awaiting-deploy"
    # conclusion = None
    # run_id = None
    # waits = 0
    # while status != "completed" and waits < 60:
    #     waits += 1
    #     run = find_run(head_sha, plugin_config, run_id=run_id)
    #     if run is None:
    #         await db.execute_write_fn(updater(status, conclusion=conclusion))
    #         time.sleep(5)
    #         continue

    #     try:
    #         run_id = run["id"]
    #         status = run["status"]
    #         conclusion = run["conclusion"]
    #     except KeyError as e:
    #         print(f"KeyError: {e}")
    #         continue
    #     await db.execute_write_fn(updater(status, conclusion=conclusion))
    #     time.sleep(5)

    # if waits == 60:
    #     conclusion = "timeout"

    # print("Deploy complete", status, conclusion)
    # await db.execute_write_fn(updater(
    #     status, conclusion=conclusion,
    #     completed=str(datetime.datetime.utcnow())
    # ))

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

    print("Returning HTML")
    return Response.html(
        await datasette.render_template(
            "git_importer_done.html", {
                "filename": filename,
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
