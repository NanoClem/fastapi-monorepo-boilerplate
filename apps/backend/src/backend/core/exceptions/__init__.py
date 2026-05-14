from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import handlers
from .customs import AppException


def register_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers to the FastAPI application.

    Args:
        app (FastAPI): FastAPI application instance to register exception handlers with.
    """
    app.add_exception_handler(AppException, handlers.app_exception_handler)  # ty:ignore[invalid-argument-type]
    app.add_exception_handler(Exception, handlers.unhandled_exception_handler)
    app.add_exception_handler(StarletteHTTPException, handlers.http_exception_handler)  # ty:ignore[invalid-argument-type]

    app.add_exception_handler(
        RequestValidationError,
        handlers.validation_exception_handler,  # ty:ignore[invalid-argument-type]
    )
