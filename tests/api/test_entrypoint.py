import pytest

from app.settings import settings
from app import app


@pytest.mark.asyncio
async def test_entrypoint_verison(monkeypatch, client):
    monkeypatch.setattr(settings.app, 'build_id', 'abcdefg')
    monkeypatch.setattr(app, '__version__', '1.2.3')

    res = await client.get('/')
    data = res.json()

    assert res.status_code == 200
    assert data['version'] == '1.2.3'
    assert data['build'] == 'abcdefg'
