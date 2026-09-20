from enum import StrEnum, auto


class Environment(StrEnum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    # add more as needed


class LogLevel(StrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class ErrorCode(StrEnum):
    """Standardized error codes for API responses."""

    CONFLICT = auto()
    NOT_FOUND = auto()
    NOT_AUTHENTICATED = auto()
    VALIDATION_ERROR = auto()
    INTERNAL_ERROR = auto()
    SERVICE_UNAVAILABLE = auto()
    FORBIDDEN = auto()
    BAD_REQUEST = auto()
    TOO_MANY_REQUESTS = auto()
    REQUEST_TIMEOUT = auto()
    GATEWAY_TIMEOUT = auto()
    BAD_GATEWAY = auto()
    METHOD_NOT_ALLOWED = auto()
