import logging
import asyncio # noqa

from app.settings import settings # noqa
from app.main import app # noqa

logging.root.setLevel(logging.DEBUG)

# Functions added to this file will be available inside the console script

print("""
To run asyncio code (debug is optional):
>>> asyncio.run(my_async_function(), debug=True)

""")