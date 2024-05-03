from fastapi import Request
from syncify.app.scripts.system_logger import logger
from .config import settings

class RequestLoggerMiddleware:
    def __init__(self, logger: logger):
        self.logger = logger

    async def __call__(self, request: Request, call_next):
        # Log request details
        request_details = {
            "time": settings.get_local_time_with_timezone(),
            "ip_address": request.client.host,
            "method": request.method,
            "url": request.url._url,
            "params": dict(request.query_params),
        }
        self.logger.info(f"Request: {request_details}")

        response = await call_next(request)

        return response
