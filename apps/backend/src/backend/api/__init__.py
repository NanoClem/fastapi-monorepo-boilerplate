from fastapi import APIRouter

from ..core.config import configs
from ..core.schemas import HealthCheckResponse
from .v1 import router as v1_router

router = APIRouter()
router.include_router(v1_router)


@router.get("/healthcheck", include_in_schema=False)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        title=configs.app.APP_NAME,
        version=configs.app.VERSION,
        description=configs.app.DESCRIPTION,
    )
