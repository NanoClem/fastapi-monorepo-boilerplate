from fastapi import APIRouter

from ..core.config import app_config
from ..core.schemas import HealthCheckResponse
from .v1 import router as v1_router

router = APIRouter()
router.include_router(v1_router)


@router.get("/healthcheck", include_in_schema=False)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        title=app_config.APP_NAME,
        version=app_config.VERSION,
        description=app_config.DESCRIPTION,
    )
