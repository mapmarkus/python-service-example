# ENV Variables

## AppSettings
Generic app settings

| Name | Description | Default |
| ---- | ---- | ---- |
| APP_PORT | Application port. Only used by uvicorn process. If empty, the server will listen in port 80 |  |
| APP_BUILD_ID | Build id | latest |
| APP_LOG_LEVEL | Log level | info |

## RedisSettings
Redis connection settings.

<sup>(1) Leave or set empty to disable redis</sup>

<sup>(2) Variables **important in production**</sup>

| Name | Description | Default |
| ---- | ---- | ---- |
| REDIS_HOST <sup>(1)</sup> | Redis host. |  |
| REDIS_PORT |  |  |
| REDIS_DB |  |  |
| REDIS_PASSWORD |  |  |
| SERVICE_REDIS_MIN_POOL_SIZE <sup>(2)</sup> | Minimum size of connection pool | 1 |
| SERVICE_REDIS_MAX_POOL_SIZE <sup>(2)</sup> | Maximum size of connection pool | 10 |

## UvicornSettings
Postgres settings

<sup>(1) **In development only**</sup>

<sup>(2) **In production only**</sup>

| Name | Description | Default |
| ---- | ---- | ---- |
| SERVER_RELOADER <sup>(1)</sup> | Use reloader | False |
| SERVER_CONCURRENCY <sup>(2)</sup> | Worker processes | 1 |

