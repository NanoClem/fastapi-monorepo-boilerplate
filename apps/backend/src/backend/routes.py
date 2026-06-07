from fastapi import APIRouter

from .common.schemas import HealthCheckResponse
from .core.config import app_config

router = APIRouter()


@router.get("/health", include_in_schema=False)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        title=app_config.APP_NAME,
        version=app_config.VERSION,
        description=app_config.DESCRIPTION,
    )
