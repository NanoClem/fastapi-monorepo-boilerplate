import copy
import logging
import re
from typing import Any


class SensitiveDataFilter(logging.Filter):
    """Log filter that masks sensitive fields in the log record message and its extra attributes."""

    # Add any keys you want to mask here
    SENSITIVE_KEYS = {
        "credentials",
        "authorization",
        "password",
        "token",
        "access_token",
        "refresh_token",
    }

    def filter(self, record: logging.LogRecord) -> bool:
        record.args = self._mask_args(record.args)
        record.msg = self._mask_msg(record.msg)
        return True

    def _mask_args(self, args: Any) -> Any:
        if isinstance(args, tuple):
            return tuple(self._mask_args(arg) for arg in args)

        if isinstance(args, dict):
            new_args = args.copy()

            for key, value in args.items():
                if key.lower() in self.SENSITIVE_KEYS:
                    new_args[key] = "********"
                elif isinstance(value, dict):
                    new_args[key] = self._mask_args(value)

            return new_args

        return args

    def _mask_msg(self, message: str | Any) -> str | Any:
        msg = copy.deepcopy(message)

        if isinstance(msg, dict):
            msg = self._mask_args(msg)

        if isinstance(msg, str):
            # replace common patterns like "password=123"
            for key in self.SENSITIVE_KEYS:
                pattern = rf"({key}=)([^&\s,]+)"
                msg = re.sub(pattern, r"\1********", msg, flags=re.IGNORECASE)

        return msg
