from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .common.types import Environment
from .core.config import AppConfig, app_config
from .core.database import db_manager
from .core.exceptions import register_exception_handlers
from .core.logging import setup_logging
from .middlewares import register_middlewares
from .routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # On startup
    setup_logging(app_config.ENVIRONMENT)
    await db_manager.initialize()

    yield

    # On shutdown
    await db_manager.close()


def create_app(configs: AppConfig, **kwargs) -> FastAPI:
    """Factory function that creates and configures a FastAPI application based on the provided configs.

    Args:
        configs (AppConfig): Configuration for the FastAPI application.

    Returns:
        FastAPI: A fully configured FastAPI application instance.
    """
    environment = configs.ENVIRONMENT
    kwargs.update(configs.fastapi_kwargs)

    # Avoid exposing swagger docs and openapi endpoints in production
    if environment == Environment.PRODUCTION:
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    app = FastAPI(lifespan=lifespan, **kwargs)
    app.include_router(api_router)

    # Register core components
    register_middlewares(app)
    register_exception_handlers(app)

    if environment != Environment.PRODUCTION:

        @app.get("/", include_in_schema=False)
        async def doc_redirect() -> RedirectResponse:
            return RedirectResponse("/docs")

    return app


app = create_app(app_config)
