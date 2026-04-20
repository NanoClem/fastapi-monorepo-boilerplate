from pydantic import Field

from ..core.config import CustomBaseSettings


class MiddlewareConfig(CustomBaseSettings):
    """Settings to be injected in middlewares at app configuration."""

    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = Field(default_factory=list[str])
    CORS_ALLOW_ORIGIN_REGEX: str | None = None


middleware_config = MiddlewareConfig()
