from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import MiddlewareConfig, middleware_config
from .log import LoggingMiddleware


def register_middlewares(
    app: FastAPI, configs: MiddlewareConfig = middleware_config
) -> None:
    # Logging
    app.add_middleware(LoggingMiddleware)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=configs.CORS_ALLOW_ORIGINS,
        allow_origin_regex=configs.CORS_ALLOW_ORIGIN_REGEX,
        allow_methods=configs.CORS_ALLOW_METHODS,
        allow_headers=configs.CORS_ALLOW_HEADERS,
        allow_credentials=True,
    )
