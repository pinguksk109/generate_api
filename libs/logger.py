import logging, logging.config
from libs.log_config import LOG_CONFIG

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger("uvicorn.error")
