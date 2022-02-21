from httpx import AsyncClient
from asgi_lifespan import LifespanManager
import pytest

from app.app import app
from app.store import store as STORE


@pytest.fixture
async def app_loop():
    # All test that use this fixture will have access to app lifespan
    # (startup and  shutdown)
    async with LifespanManager(app):
        yield


@pytest.fixture
async def client(app_loop):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def store(app_loop):
    yield STORE
