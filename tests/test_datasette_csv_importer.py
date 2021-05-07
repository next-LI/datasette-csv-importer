from datasette.app import Datasette
import asyncio
from asgi_lifespan import LifespanManager
import json
import pytest
import httpx
import sqlite_utils


@pytest.mark.asyncio
async def test_lifespan():
    ds = Datasette([], memory=True)
    app = ds.app()
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app) as client:
            response = await client.get("http://localhost/")
            assert 200 == response.status_code


@pytest.mark.asyncio
@pytest.mark.parametrize("auth", [True, False])
async def test_menu(auth):
    ds = Datasette([], memory=True)
    app = ds.app()
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app) as client:
            cookies = {}
            if auth:
                cookies = {"ds_actor": ds.sign({"a": {"id": "root"}}, "actor")}
            response = await client.get("http://localhost/", cookies=cookies)
            assert 200 == response.status_code
            if auth:
                assert "/-/csv-importer" in response.text
            else:
                assert "/-/csv-importer" not in response.text


@pytest.mark.asyncio
async def test_permissions(tmpdir):
    path = str(tmpdir / "data.db")
    db = sqlite_utils.Database(path)["foo"].insert({"hello": "world"})
    ds = Datasette([path])
    app = ds.app()
    async with httpx.AsyncClient(app=app) as client:
        response = await client.get("http://localhost/-/csv-importer")
        assert 403 == response.status_code
    # Now try with a root actor
    async with httpx.AsyncClient(app=app) as client2:
        response2 = await client2.get(
            "http://localhost/-/csv-importer",
            cookies={"ds_actor": ds.sign({"a": {"id": "root"}}, "actor")},
            allow_redirects=False,
        )
        assert 403 != response2.status_code

@pytest.mark.asyncio
async def test_upload(tmpdir):
    path = str(tmpdir / "data.db")
    db = sqlite_utils.Database(path)
    datasette = Datasette([path])
    cookies = {"ds_actor": datasette.sign({"a": {"id": "root"}}, "actor")}

    # First test the upload page exists
    async with httpx.AsyncClient(app=datasette.app()) as client:
        response = await client.get("http://localhost/-/csv-importer", cookies=cookies)
        assert 200 == response.status_code
        signature = b'<form id="file-form" action="/-/csv-importer" method="post"'
        assert signature in response.content
        csrftoken = response.cookies["ds_csrftoken"]
        cookies["ds_csrftoken"] = csrftoken

        # Now try uploading a file, setting XHR flag
        files = {"csv": ("dogs.csv", "name,age\nCleo,5\nPancakes,4", "text/csv")}
        response = await client.post(
            "http://localhost/-/csv-importer",
            cookies=cookies,
            data={"csrftoken": csrftoken, "xhr": "1"},
            files=files,
        )
        assert 200 == response.status_code
        response_json = response.json()
        assert response_json
        status_db = response_json["status_database_path"]
        task_id = response_json["task_id"]
        print("response_json", response_json)

        # NOTE: This would be for a non-XHR test
        # assert b"<h1>Upload in progress</h1>" in response.content

        # Now things get tricky... the upload is running in a thread, so poll for completion
        await asyncio.sleep(1)
        response = await client.get(
            f"http://localhost/{status_db}/_csv_importer_progress_.json?id={task_id}&_shape=array",
            cookies=cookies,
        )
        rows = response.json()
        assert 1 == len(rows)
        row = rows[0]
        assert not row.get("completed")
        assert "id" in row and row["id"]
        assert row.get("started")
        assert row.get("filename") == "dogs.csv"
        assert row.get("dbname") == "dogs"
        print("First status", row)

        completed = row["completed"]
        status = response.status_code

        # poll until complete
        remaining_tries = 5
        while not completed and status == 200:
            response = await client.get(
                f"http://localhost/{status_db}/_csv_importer_progress_.json?id={task_id}&_shape=array",
                cookies=cookies,
            )
            rows = response.json()
            assert 1 == len(rows)
            row = rows[0]
            print("row", row)
            await asyncio.sleep(1)
            assert remaining_tries
            remaining_tries -= 1

        assert row.get("completed")
        # check for success code
        assert row["exitcode"] == 0
        # check for status messages
        assert "status" in row and row.get("status")
        assert "message" in row and row.get("message")
        assert "output" in row and row.get("output")
