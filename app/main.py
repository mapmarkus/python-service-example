import logging

from app.app import app  # noqa (re-export for uvicorn)
from app.util import get_log_level
from app.settings import settings

# Reset logger first
for handler in logging.root.handlers:
    logging.root.removeHandler(handler)

# Set main logger
logging.basicConfig(
    level=get_log_level(settings.app.log_level),
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
