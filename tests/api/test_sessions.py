from uuid import uuid4
import pytest


@pytest.mark.asyncio
@pytest.mark.skip(reason="Not implemented")
async def test_get_session(client):
    res = await client.get('/sessions/valid-id')

    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_session_id_must_by_valid_uuid(client):
    res = await client.get('/sessions/xxx')

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_get_session_id_not_found(client):
    res = await client.get(f'/sessions/{uuid4()}')

    assert res.status_code == 404
