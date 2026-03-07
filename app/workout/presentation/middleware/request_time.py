import time
from collections.abc import Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        start_time = time.perf_counter()

        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        if process_time < 1:
            time_str = f"{process_time * 1000:.2f}ms"
        else:
            time_str = f"{process_time:.2f}s"
        response.headers["X-Process-Time"] = time_str

        logger.info(
            f"Completed {request.method} {request.url} | Status: {response.status_code} | Time: {time_str}"
        )
        return response
