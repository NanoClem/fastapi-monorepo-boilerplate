from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from ..types import ErrorCode
from .customs import AppException


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "error_code": ErrorCode.INTERNAL_ERROR,
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for Pydantic validation errors"""

    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({"field": field, "message": error["msg"], "type": error["type"]})

    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "error_code": ErrorCode.VALIDATION_ERROR,
            "message": "Request validation failed",
            "details": {"errors": errors},
        },
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler for standard HTTP exceptions"""
    error_code_map = {
        400: ErrorCode.BAD_REQUEST,
        401: ErrorCode.NOT_AUTHENTICATED,
        403: ErrorCode.FORBIDDEN,
        404: ErrorCode.NOT_FOUND,
        405: ErrorCode.METHOD_NOT_ALLOWED,
        408: ErrorCode.REQUEST_TIMEOUT,
        409: ErrorCode.CONFLICT,
        429: ErrorCode.TOO_MANY_REQUESTS,
        500: ErrorCode.INTERNAL_ERROR,
        502: ErrorCode.BAD_GATEWAY,
        503: ErrorCode.SERVICE_UNAVAILABLE,
        504: ErrorCode.GATEWAY_TIMEOUT,
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error_code": error_code_map.get(exc.status_code, "HTTP_ERROR"),
            "message": str(exc.detail),
        },
    )
