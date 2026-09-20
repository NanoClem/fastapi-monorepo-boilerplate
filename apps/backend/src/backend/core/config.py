from typing import Any

from pydantic import EmailStr

from backend import __description__, __version__
from backend.common.config import CustomBaseSettings
from backend.common.types import Environment, LogLevel


class AppConfig(CustomBaseSettings):
    """FastAPI app metadata settings."""

    APP_NAME: str = "FastAPI backend app"
    LICENSE_NAME: str = "MIT"
    CONTACT_NAME: str | None = None
    CONTACT_EMAIL: EmailStr | None = None
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    @property
    def DEBUG(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT

    @property
    def VERSION(self) -> str:
        return __version__ if not self.DEBUG else "dev"

    @property
    def DESCRIPTION(self) -> str:
        return __description__

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "title": self.APP_NAME,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "contact": {"name": self.CONTACT_NAME, "email": self.CONTACT_EMAIL},
            "license_info": {"name": self.LICENSE_NAME},
            "debug": self.DEBUG,
            "swagger_ui_parameters": {
                "persistAuthorization": self.DEBUG,
            },
        }


class LoggingConfig(CustomBaseSettings):
    """Settings related to logging configuration."""

    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_DIR: str = "logs"               # production only
    LOG_SIZE: int = 10 * 1024 * 1024    # 10 MB per file
    LOG_BACKUP_COUNT: int = 5           # number of backup files to keep
    LOG_ENCODING: str = "utf-8"


app_config = AppConfig()
logging_config = LoggingConfig()
