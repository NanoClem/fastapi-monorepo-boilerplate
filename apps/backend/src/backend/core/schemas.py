from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, field_serializer

from .types import ErrorCode


class CustomBaseModel(BaseModel):
    """Custom Pydantic base model with custom configurations and serializers."""

    model_config = ConfigDict(
        populate_by_name=True,
    )

    @field_serializer("*", when_used="json", check_fields=False)
    def _serialize_datetimes(self, value: Any) -> Any | str:
        if not isinstance(value, datetime):
            return value

        if value.tzinfo is None:
            value = value.replace(tzinfo=ZoneInfo("UTC"))

        return value.strftime("%Y-%m-%dT%H:%M:%S%z")


class PaginatedResponse[T: CustomBaseModel](CustomBaseModel):
    """Generic pagination response model."""

    total: int
    page: int
    size: int
    items: list[T]


class HealthCheckResponse(CustomBaseModel):
    title: str
    version: str
    description: str


class ErrorResponse(CustomBaseModel):
    message: str
    status: int
    error_code: ErrorCode
    details: dict[str, Any] | None = None
