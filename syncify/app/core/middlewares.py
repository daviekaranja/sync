from fastapi import Request
from fastapi.responses import RedirectResponse
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

    # Define middleware function


async def check_authentication(request: Request, call_next, app):
    # Check if user is trying to access allowed routes
    allowed_routes = [
        '/',
    ]
    if request.url.path in allowed_routes:
        # Proceed with the request for allowed routes
        response = await call_next(request)
        return response

    # Check if user is logged in
    user_id = request.session.get('user_id')
    if not user_id:
        # Redirect to '/' if user is not logged in
        return RedirectResponse(url='/')

    # User is logged in, proceed with the request
    response = await call_next(request)
    return response
