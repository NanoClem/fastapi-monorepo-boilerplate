import os
from typing import Any

from ..core.types import Environment
from .config import LoggingConfig
from .filters import SensitiveDataFilter


def build_log_config(environment: Environment, config: LoggingConfig) -> dict[str, Any]:
    is_prod = environment == Environment.PRODUCTION

    return {
        "version": 1,
        "disable_existing_loggers": True,
        "filters": {
            "masking": {
                "()": SensitiveDataFilter,
            }
        },
        "formatters": {
            "pretty": {
                "format": '%(asctime)s - [%(levelname)s] %(client)s %(status_code)s - "%(method)s %(path)s" | %(duration_ms)s ms',
                "datefmt": "%H:%M:%S",
            },
            "json": {
                "()": "json_log_formatter.JSONFormatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S%z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "pretty",
                "filters": ["masking"],
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",  # use TimedRotatingFileHandler if you prefer time-based rotation
                "filename": os.path.join(config.LOG_DIR, "app.json"),
                "formatter": "json",
                "filters": ["masking"],
                "maxBytes": config.LOG_SIZE,
                "backupCount": config.LOG_BACKUP_COUNT,
                "encoding": config.LOG_ENCODING,
            },
        },
        "loggers": {
            "app_logger": {
                "handlers": ["file" if is_prod else "console"],
                "level": config.LOG_LEVEL,
                "propagate": False,
            },
        },
    }
