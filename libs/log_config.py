LOG_APPLICATION_OUTPUT_PATH = "logs/application.log"
LOG_ACCESS_OUTPUT_PATH = "logs/access.log"

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s.%(msecs)03d][%(levelname)s][%(process)s] %(module)s %(funcName)s:%(lineno)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {
            "format": "[%(asctime)s.%(msecs)03d][%(process)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": LOG_APPLICATION_OUTPUT_PATH,
            "encoding": "utf-8",
            "when": "MIDNIGHT",
            "backupCount": 7,
            "level": "INFO",
        },
        "app": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "default",
            "filename": LOG_APPLICATION_OUTPUT_PATH,
            "encoding": "utf-8",
            "when": "MIDNIGHT",
            "backupCount": 7,
            "level": "INFO",
        },
        "access": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "access",
            "filename": LOG_ACCESS_OUTPUT_PATH,
            "encoding": "utf-8",
            "when": "MIDNIGHT",
            "backupCount": 7,
            "level": "INFO",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "gunicorn": {"propagate": True},
        "gunicorn.access": {"propagate": True},
        "gunicorn.error": {"propagate": True},
        "uvicorn": {"propagate": True},
        "uvicorn.access": {"handlers": ["access"], "propagate": False},
        "uvicorn.error": {"handlers": ["app"], "propagate": False},
    },
}
