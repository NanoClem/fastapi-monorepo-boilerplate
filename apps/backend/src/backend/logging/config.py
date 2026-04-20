from ..core.config import CustomBaseSettings
from .types import LogLevel


class LoggingConfig(CustomBaseSettings):
    """Settings related to logging configuration."""

    LOG_LEVEL: str = LogLevel.INFO
    LOG_DIR: str = "logs"  # production only
    LOG_SIZE: int = 10 * 1024 * 1024  # 10 MB per file
    LOG_BACKUP_COUNT: int = 5  # number of backup files to keep
    LOG_ENCODING: str = "utf-8"


logging_config = LoggingConfig()
