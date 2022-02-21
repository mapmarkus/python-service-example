import pytest


@pytest.mark.asyncio
async def test_read_health(client):
    res = await client.get('/healthz')
    data = res.json()

    assert res.status_code == 200
    assert data == {'message': 'ok'}
