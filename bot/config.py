import importlib
import os
import sys
from logging import getLogger
logger = getLogger(__name__)

def load_config():
    conf_name = os.environ.get('TG_CONF')
    if conf_name is None:
        conf_name = 'development'
    try:
        r = importlib.import_module(f'settings.{conf_name}')
        logger.debug(f'Loaded config is |{conf_name}| OK')
        return r
    except (TypeError, ValueError, ImportError):
        logger.error(f'Invalid config = {conf_name}')
        sys.exit(1)


