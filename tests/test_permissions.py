from datasette.app import Datasette
import sqlite_utils
import pytest


@pytest.fixture
def datasette(tmpdir):
    path1 = str(tmpdir / "data.db")
    db = sqlite_utils.Database(path1)
    db["creatures"].insert_all(
        [
            {"name": "Cleo", "description": "A medium sized dog"},
            {"name": "Siroco", "description": "A troublesome Kakapo"},
        ]
    )
    path2 = str(tmpdir / "another.db")
    db = sqlite_utils.Database(path2)
    db["things"].insert_all(
        [
            {"name": "Pencil", "description": "A writing instrument"},
            {"name": "Wheel", "description": "A basic tool"},
        ]
    )
    datasette = Datasette([path1, path2])
    return datasette


async def permission_allowed(*args, **kwargs):
    return True


@pytest.mark.asyncio
async def test_can_access_with_permission(datasette):
    datasette.permission_allowed = permission_allowed
    response = await datasette.client.get("/-/csv-importer")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_cant_access_without_permission(datasette):
    async def perm_check(actor, action, *args, **kwargs):
        if action == "csv-importer":
            return False
        return True
    datasette.permission_allowed = perm_check
    response = await datasette.client.get("/-/csv-importer")
    assert response.status_code == 403
