from datetime import datetime
from uuid import uuid4
import pytest

from app.constants import SESSION_MAX_AGE, STORE_KEY


@pytest.fixture
def dummy_session():
    mock_uuid = '579e9e7c-f8cb-4a3f-9c22-03b83c469052'
    return {
        'id': mock_uuid,
        'data': {'test': True},
        'created_at': 1,
        'expires_at': 2
    }


@pytest.mark.asyncio
async def test_get_session(client, store, dummy_session):
    await store.set_json(STORE_KEY.format(session_id=dummy_session['id']), dummy_session)

    res = await client.get(f'/sessions/{dummy_session["id"]}')
    data = res.json()

    assert res.status_code == 200
    assert data['id'] == dummy_session['id']
    assert data['data'] == {'test': True}
    assert data['created_at'] == 1
    assert data['expires_at'] == 2


@pytest.mark.asyncio
async def test_get_session_id_must_by_valid_uuid(client):
    res = await client.get('/sessions/xxx')

    assert res.status_code == 422


@pytest.mark.asyncio
async def test_get_session_id_not_found(client):
    res = await client.get(f'/sessions/{uuid4()}')

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_post_session(client, store, dummy_session, mocker):
    mock_datetime = mocker.patch('app.api.routes.sessions.datetime')
    mock_now = datetime.now()
    mock_datetime.now.return_value = mock_now

    res = await client.post('/sessions/', json=dummy_session)
    data = res.json()

    assert res.status_code == 200
    assert data['id'] == dummy_session['id']
    assert data['data'] == {'test': True}
    assert data['created_at'] == int(mock_now.timestamp())
    assert data['expires_at'] == int((mock_now + SESSION_MAX_AGE).timestamp())
    assert await store.exists(STORE_KEY.format(session_id=dummy_session['id']))
