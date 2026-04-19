from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .api import router as api_router
from .core.config import GlobalConfig, configs
from .core.types import Environment
from .middlewares import setup_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # On startup

    yield

    # On shutdown
    # ...


def create_app(configs: GlobalConfig, **kwargs) -> FastAPI:
    """Factory function that creates and configures a FastAPI application based on the provided configs.

    Args:
        configs (GlobalConfig): Configuration for the FastAPI application.

    Returns:
        FastAPI: A fully configured FastAPI application instance.
    """
    environment = configs.app.ENVIRONMENT
    kwargs.update(configs.app.fastapi_kwargs)

    # Avoid exposing swagger docs and openapi endpoints in production
    if environment == Environment.PRODUCTION:
        kwargs.update({"docs_url": None, "redoc_url": None, "openapi_url": None})

    app = FastAPI(lifespan=lifespan, **kwargs)

    # Routes
    app.include_router(api_router)

    # Middlewares
    setup_middlewares(app, configs.middleware)

    if environment != Environment.PRODUCTION:

        @app.get("/", include_in_schema=False)
        async def doc_redirect() -> RedirectResponse:
            return RedirectResponse("/docs")

    return app


app = create_app(configs)
