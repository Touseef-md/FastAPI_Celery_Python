from fastapi import Request
from app.tasks import log_access

async def log_requests(request: Request, call_next):
    """
    Middleware function to log incoming HTTP requests using Celery task.

    This function is designed to be used as a FastAPI middleware. It logs the HTTP method,
    URL path, and query parameters of each incoming request using a Celery task.

    Parameters:
    - request (Request): The FastAPI Request object representing the incoming HTTP request.
    - call_next (Callable): A coroutine function that will be called to process the next middleware or the actual endpoint.

    Returns:
    - response (Response): The HTTP response returned by the next middleware or the actual endpoint.
    """

    text = request.method + " " + request.url.path
    if request.url.query:
        text += "?" + request.url.query
    log_access.delay(text)

    response = await call_next(request)
    return response
