import json
import logging
import time
import uuid

from fastapi import Request, Response, status
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger("app_logger")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = str(uuid.uuid4())
        client = request.client.host if request.client else "unknown"
        req_body = json.loads(await request.body() or "{}")

        logger.info(
            "Incoming request",
            extra={
                "request_id": request_id,
                "client": client,
                "status_code": status.HTTP_100_CONTINUE,
                "method": request.method,
                "path": request.url.path,
                "body": req_body,
                "duration_ms": 0,
            },
        )

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 3)

        res_body = [chunk async for chunk in response.body_iterator]  # ty:ignore[unresolved-attribute]
        response.body_iterator = iterate_in_threadpool(iter(res_body))  # ty:ignore[unresolved-attribute]
        res_body = res_body[0].decode()

        if response.headers.get("Content-Type") == "application/json":
            res_body = json.loads(res_body)

        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "client": client,
                "status_code": response.status_code,
                "method": request.method,
                "path": request.url.path,
                "body": res_body,
                "duration_ms": duration_ms,
            },
        )

        response.headers["X-Request-ID"] = request_id
        return response
