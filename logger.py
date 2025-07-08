import sys
import io

import logging
import logging.config

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": (
                "[%(asctime)s.%(msecs)03d][%(levelname)s][%(process)s] "
                "%(name)s %(funcName)s:%(lineno)s - %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "ai_log_test": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "boto3": {
            "handlers": ["console"],
            "propagate": False,
        },
        "botocore": {
            "handlers": ["console"],
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("ai_log_test")
