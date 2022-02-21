from fastapi import FastAPI

from app import __version__
from app.api import __version__ as __api_version__
from app.api.api import api_router
from app.api.schemas.message import Message
from app.middleware import RequestLoggingMiddleware
from app.settings import settings
from app.store import store


app = FastAPI(title='Service API', redoc_url=None)


# Middlewares

app.add_middleware(RequestLoggingMiddleware)


# Lifecycle

@app.on_event('startup')
async def startup():
    await store.connect()


@app.on_event('shutdown')
async def shutdown():
    await store.disconnect()


# Entry point and health routes

@app.get('/healthz', tags=['health'], response_model=Message)
def show_health_info():
    """Health route to test if the service is running
    """
    return Message.Ok()


@app.get('/', tags=['entrypoint'])
def show_version():
    """Entrypoint information
    """
    return {
        'version': __version__,
        'api_version': __api_version__,
        'build': settings.app.build_id
    }


# Api routes

app.include_router(api_router)
