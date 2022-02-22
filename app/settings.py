from typing import Annotated, Optional

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    """Generic app settings"""

    port: Annotated[Optional[int], Field(
        description='Application port. Only used by uvicorn process. '
        'If empty, the server will listen in port 80')] = None
    build_id: Annotated[Optional[str], Field(
        description='Build id')] = 'latest'
    dev_mode: Annotated[bool, Field(
        description='Dev mode', hidden=True)] = False
    test_mode: Annotated[bool, Field(
        description='Test model', hidden=True)] = False
    log_level: Annotated[str, Field(
        description='Log level',
        valid_options=['debug', 'info', 'warning', 'error'])] = 'info'

    class Config:
        env_prefix = 'APP_'


# Example of PostgresSettings
# class PostgresSettings(BaseSettings):
#     """Postgres settings

#     <sup>(1) Variables **important in production**</sup>
#     """
#     user: Annotated[str, Field(description='Postgres user')] = 'postgres'
#     password: Annotated[str, Field(description='Postgres password')] = 'postgres'
#     host: Annotated[str, Field(description='Postgres host')] = 'db'
#     port: Annotated[str, Field(description='Postgres port')] = '5432'
#     name: Annotated[str, Field(description='Database name')] = 'main-db'
#     min_pool_size: Annotated[
#         Optional[int], Field(description='Minimum size of connection pool', note=1)]
#     max_pool_size: Annotated[
#         Optional[int], Field(description='Maximum size of connection pool', note=1)]
#     force_rollback: Annotated[
#         bool, Field(description='Force rollback (tests)', hidden=True)] = False

#     @property
#     def url(self):
#         return (
#             f'postgresql://{self.user}:{self.password}'
#             f'@{self.host}:{self.port}/{self.name}'
#         )

#     @property
#     def kwargs(self):
#         return self.dict(
#             include={'min_pool_size', 'max_pool_size', 'force_rollback'},
#             exclude_unset=True)

#     class Config:
#         env_prefix = 'DB_'
#         fields = {
#             'force_rollback': {'env': 'service_test_mode'}
#         }


class RedisSettings(BaseSettings):
    """Redis connection settings.

    <sup>(1) Leave or set empty to disable redis</sup>

    <sup>(2) Variables **important in production**</sup>
    """

    host: Annotated[Optional[str], Field(description='Redis host.', note=1)]
    port: Optional[str]
    db: Optional[int]
    password: Optional[str]
    minsize: Annotated[
        Optional[int], Field(
            description='Minimum size of connection pool', note=2)] = 1
    maxsize: Annotated[
        Optional[int], Field(
            description='Maximum size of connection pool', note=2)] = 10
    flush_on_disconnect: Annotated[
        bool, Field(
            description='Flush db when the connection closes', hidden=True)] = False

    @property
    def url(self):
        if self.host is None:
            return 'memory://'

        if self.port:
            address = f'redis://{self.host}:{self.port}'
        else:
            address = f'redis://{self.host}'

        options = self.dict(exclude={'host', 'port'}, exclude_none=True)
        options['encoding'] = 'utf-8'

        if self.flush_on_disconnect:
            # Use db 9 for tests
            options['db'] = 9

        query = '&'.join([f'{k}={v}' for k, v in options.items()])

        return address + '?' + query

    class Config:
        env_prefix = 'REDIS_'
        fields = {
            'minsize': {'env': 'service_redis_min_pool_size'},
            'maxsize': {'env': 'service_redis_max_pool_size'},
            'flush_on_disconnect': {'env': 'serivce_test_mode'}
        }


class UvicornSettings(BaseSettings):
    """Postgres settings

    <sup>(1) **In development only**</sup>

    <sup>(2) **In production only**</sup>
    """

    reloader: Annotated[
        bool, Field(description='Use reloader', note=1)] = False
    concurrency: Annotated[
        Optional[int], Field(description='Worker processes', note=2)] = 1

    class Config:
        env_prefix = 'SERVER_'
        fields = {
            'min': {'env': 'min_pool_size'},
            'max': {'env': 'max_pool_size'}
        }


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    redis: RedisSettings = RedisSettings()
    uvicorn: UvicornSettings = UvicornSettings()

    #postgres: PostgresSettings = PostgresSettings()


settings = Settings()
