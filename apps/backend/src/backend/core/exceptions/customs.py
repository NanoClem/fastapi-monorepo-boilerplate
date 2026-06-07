from typing import Any

from backend.common.types import ErrorCode


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details


class NotFoundError(AppException):
    def __init__(
        self,
        resource: str,
        resource_id: Any,
        message: str | None = None,
    ):
        super().__init__(
            message=message or f"{resource} with ID {resource_id} not found",
            status_code=404,
            error_code=ErrorCode.NOT_FOUND,
            details={"resource": resource, "resource_id": resource_id},
        )


class ConflictError(AppException):
    def __init__(
        self,
        resource: str,
        message: str | None = None,
    ):
        super().__init__(
            message=message or f"{resource} already exists",
            status_code=409,
            error_code=ErrorCode.CONFLICT,
            details={"resource": resource},
        )


class ValidationError(AppException):
    def __init__(
        self,
        field: str,
        message: str,
        value: Any = None,
    ):
        super().__init__(
            message=f"Validation error on field '{field}': {message}",
            status_code=422,
            error_code=ErrorCode.VALIDATION_ERROR,
            details={"field": field, "value": value},
        )


class ForbiddenError(AppException):
    def __init__(
        self,
        action: str,
        resource: str,
        message: str | None = None,
    ):
        super().__init__(
            message=message or f"Cannot {action} on {resource}",
            status_code=403,
            error_code=ErrorCode.FORBIDDEN,
            details={"action": action, "resource": resource},
        )


class ExternalServiceError(AppException):
    def __init__(
        self,
        service: str,
        message: str | None = None,
    ):
        super().__init__(
            message=message or f"External service '{service}' is unavailable",
            status_code=503,
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            details={"service": service},
        )
