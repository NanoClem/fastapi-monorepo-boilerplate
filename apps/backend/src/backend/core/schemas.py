from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, field_serializer


class CustomBaseModel(BaseModel):
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


class HealthCheckResponse(CustomBaseModel):
    title: str
    version: str
    description: str
