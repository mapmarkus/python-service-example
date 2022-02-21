import pytest
import json

from app.settings import settings
from app.store import Store


@pytest.fixture(params=['memory://', settings.redis.url])
async def store(request):
    async with Store(request.param) as st:
        yield st


@pytest.mark.asyncio
async def test_store_get_json(store):
    await store.backend.set('test', json.dumps(dict(x=1, y=2)))

    assert await store.get_json('test') == {'x': 1, 'y': 2}

    await store.backend.set('test', '')

    assert await store.get_json('test') == {}


@pytest.mark.asyncio
async def test_store_set_json(store):
    await store.set_json('test', {'x': 1, 'y': 2})

    assert await store.backend.get('test') == json.dumps(dict(x=1, y=2))

    await store.set_json('test', {})

    assert await store.backend.get('test') == '{}'


@pytest.mark.asyncio
async def test_store_get_collection_json(store):
    await store.backend.set_item('test', 'item1', json.dumps(dict(x=1, y=2)))
    await store.backend.set_item('test', 'item2', json.dumps(dict(u=3, v=4)))

    assert await store.get_collection_json('test') == {
        'item1': {'x': 1, 'y': 2}, 'item2': {'u': 3, 'v': 4}}

    assert await store.get_collection_json('other') == {}


@pytest.mark.asyncio
async def test_store_get_item_json(store):
    await store.backend.set_item('test', 'item1', json.dumps(dict(x=1, y=2)))
    await store.backend.set_item('test', 'item2', json.dumps(dict(u=3, v=4)))

    assert await store.get_item_json('test', 'item1') == {'x': 1, 'y': 2}
    assert await store.get_item_json('test', 'item2') == {'u': 3, 'v': 4}

    assert await store.get_item_json('test', 'other') == {}
    assert await store.get_item_json('other', 'item1') == {}


@pytest.mark.asyncio
async def test_store_set_item_json(store):
    await store.set_item_json('test', 'item1', dict(x=1, y=2))
    await store.set_item_json('test', 'item2', dict(u=3, v=4))

    assert await store.backend.get_item('test', 'item1') == json.dumps({'x': 1, 'y': 2})
    assert await store.backend.get_item('test', 'item2') == json.dumps({'u': 3, 'v': 4})
