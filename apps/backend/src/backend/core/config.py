from pathlib import Path
from typing import Any

from backend import __description__, __version__
from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .types import Environment


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


class MiddlewareConfig(CustomBaseSettings):
    """Settings to be injected in middlewares at app configuration."""

    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = Field(default_factory=list[str])
    CORS_ALLOW_ORIGIN_REGEX: str | None = None


class GlobalConfig(CustomBaseSettings):
    """Global app settings."""

    app: AppConfig = AppConfig()
    middleware: MiddlewareConfig = MiddlewareConfig()


configs = GlobalConfig()

