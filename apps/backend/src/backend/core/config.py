from pathlib import Path
from typing import Any

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from backend import __description__, __version__
from backend.common.types import Environment, LogLevel


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[3] / ".env",  # backend root .env file
        env_file_encoding="utf-8",
        extra="ignore",
    )


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


class DatabaseConfig(CustomBaseSettings):
    model_config = {
        **CustomBaseSettings.model_config,
        "env_prefix": "DB_",
    }

    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "db"
    DRIVER: str = "asyncpg"

    POOL_SIZE: int = 20
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    MAX_OVERFLOW: int = 10
    PREFIXED_ID_LENGTH: int = 21

    @property
    def DB_URL(self) -> str:
        return f"postgresql+{self.DRIVER}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

    @property
    def POSTGRES_INDEXES_NAMING_CONVENTION(self) -> dict[str, str]:
        return {
            "ix": "%(column_0_label)s_idx",
            "uq": "%(table_name)s_%(column_0_name)s_key",
            "ck": "%(table_name)s_%(constraint_name)s_check",
            "fk": "%(table_name)s_%(column_0_name)s_fkey",
            "pk": "%(table_name)s_pkey",
        }


class LoggingConfig(CustomBaseSettings):
    """Settings related to logging configuration."""

    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_DIR: str = "logs"  # production only
    LOG_SIZE: int = 10 * 1024 * 1024  # 10 MB per file
    LOG_BACKUP_COUNT: int = 5  # number of backup files to keep
    LOG_ENCODING: str = "utf-8"


app_config = AppConfig()
db_config = DatabaseConfig()
logging_config = LoggingConfig()
