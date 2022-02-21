import logging
import time

from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.middleware.cors import CORSMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs request details and elapsed time
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        url = request.url.path
        if request.url.query:
            url = f'{url}?{request.url.query}'

        response = await call_next(request)

        elapsed = round(round(time.time() - start_time, 4) * 1000)
        logging.info(
            f'{request.method} {url} {response.status_code} (elapsed {elapsed}ms)')

        return response


class CORSAllowAnyMiddleware(CORSMiddleware):
    """Speciall CORS middleware to allow requests from any origin.
    """

    def __init__(self):
        super().__init__(
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
