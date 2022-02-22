import logging
import typing
from urllib.parse import urlparse, parse_qsl
from pydantic import BaseModel

import aioredis

from app.util import safe_dict_json_loads, safe_dict_json_dumps
from app.settings import settings


class Backend:

    async def connect(self) -> None:
        raise NotImplementedError()

    async def disconnect(self) -> None:
        raise NotImplementedError()

    async def get(self, key: str) -> str:
        raise NotImplementedError()

    async def set(self, key: str, raw: str, *, until=None) -> None:
        raise NotImplementedError()

    async def keys(self, pattern: str = '*') -> typing.List[str]:
        raise NotImplementedError()

    async def exists(self, key: str) -> bool:
        raise NotImplementedError()

    async def get_collection(self, key: str) -> typing.Dict[str, str]:
        raise NotImplementedError()

    async def get_item(self, key: str, item: str) -> str:
        raise NotImplementedError()

    async def set_item(self, key: str, item: str, value: str) -> None:
        raise NotImplementedError()


class MemoryBackend(Backend):

    def __init__(self):
        self._dict = None

    async def connect(self) -> None:
        self._dict = {}

    async def disconnect(self) -> None:
        self._dict = None

    async def get(self, key: str) -> str:
        return self._dict.get(key, '')

    async def set(self, key: str, raw: str, *, until=None) -> None:
        self._dict[key] = raw

    # async def keys(self, pattern: str = '*') -> typing.List[str]:
    #     raise NotImplementedError()

    async def exists(self, key: str) -> bool:
        return key in self._dict

    async def get_collection(self, key: str) -> typing.Dict[str, str]:
        return self._dict.get(key, {})

    async def get_item(self, key: str, item: str) -> str:
        return self._dict.get(key, {}).get(item, None)

    async def set_item(self, key: str, item: str, value: str) -> None:
        self._dict.setdefault(key, {}).update({item: value})


class RedisBackend(Backend):
    def __init__(self, url):
        parsed_url = urlparse(url)
        options = dict(parse_qsl(parsed_url.query))
        self.options = RedisBackend.Options(**options).dict(exclude_none=True)
        self.options['address'] = f'redis://{parsed_url.netloc}'
        self._connection = None
        self.flush_on_disconnect = options.get(
            'flush_on_disconnect', 'False') == 'True'

    async def connect(self) -> None:
        self._connection = await aioredis.create_redis_pool(**self.options)
        logging.info(f'Redis connected, options: {self.options}')

    async def disconnect(self) -> None:
        if self.flush_on_disconnect:
            logging.info('Redis db flushed')
            await self._connection.flushdb()
        self._connection.close()
        await self._connection.wait_closed()
        self._connection = None

    async def set(self, key: str, raw: str, *, until=None) -> None:
        await self._connection.set(key, raw)

        if until:
            await self._connection.expireat(key, until)

    async def get(self, key: str) -> str:
        return await self._connection.get(key) or ''

    async def keys(self, pattern: str = '*') -> typing.List[str]:
        return await self._connection.keys(pattern)

    async def exists(self, key: str) -> bool:
        return await self._connection.exists(key) == 1

    async def get_collection(self, key: str) -> typing.Dict[str, str]:
        return await self._connection.hgetall(key)

    async def get_item(self, key: str, item: str) -> str:
        return await self._connection.hget(key, item) or ''

    async def set_item(self, key: str, item: str, value: str) -> None:
        await self._connection.hset(key, item, value)

    class Options(BaseModel):
        db: typing.Optional[int]
        password: typing.Optional[str]
        ssl: typing.Optional[bool]
        encoding: typing.Optional[str]
        minsize: typing.Optional[int] = 1
        maxsize: typing.Optional[int] = 10


class Store:
    def __init__(self, url: str):
        self.is_connected = False
        self.backend: Backend
        parsed_url = urlparse(url)

        if parsed_url.scheme == 'memory':
            self.backend = MemoryBackend()
        elif parsed_url.scheme == 'redis':
            self.backend = RedisBackend(url)
        else:
            raise NameError(f'{parsed_url.scheme} not supported')

    async def connect(self) -> None:
        assert not self.is_connected, 'Already connected'
        await self.backend.connect()
        self.is_connected = True

    async def disconnect(self) -> None:
        assert self.is_connected, 'Not connected'
        await self.backend.disconnect()
        self.is_connected = False

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.disconnect()

    async def set_json(
        self,
        key: str,
        json_value: typing.Dict[str, typing.Any],
        *,
        until: int = None
    ) -> None:
        assert self.is_connected, 'Not connected'
        raw_value = safe_dict_json_dumps(json_value)
        await self.backend.set(key, raw_value, until=until)

    async def get_json(
        self,
        key: str
    ) -> typing.Dict[str, typing.Any]:
        assert self.is_connected, 'Not connected'
        raw = await self.backend.get(key)
        return safe_dict_json_loads(raw)

    async def keys(self, pattern: str = '*') -> typing.List[str]:
        assert self.is_connected, 'Not connected'
        return await self.backend.keys(pattern)

    async def exists(self, key: str) -> bool:
        assert self.is_connected, 'Not connected'
        return await self.backend.exists(key)

    async def get_collection_json(
        self,
        key: str
    ) -> typing.Dict[str, typing.Dict[str, typing.Any]]:
        assert self.is_connected, 'Not connected'
        coll = await self.backend.get_collection(key)
        return {item: safe_dict_json_loads(val) for item, val in coll.items()}

    async def get_item_json(
        self,
        key: str,
        item: str
    ) -> typing.Dict[str, typing.Any]:
        assert self.is_connected, 'Not connected'
        raw = await self.backend.get_item(key, item)
        return safe_dict_json_loads(raw)

    async def set_item_json(
        self,
        key: str,
        item: str,
        value: typing.Dict[str, typing.Any]
    ) -> None:
        assert self.is_connected, 'Not connected'
        await self.backend.set_item(key, item, safe_dict_json_dumps(value))


store = Store(settings.redis.url)
