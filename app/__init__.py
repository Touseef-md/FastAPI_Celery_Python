from fastapi import FastAPI
from app.celery_utils import create_celery
from app.middlewares.logging_middleware import log_requests
from app.reviews import review_router
def create_app() -> FastAPI:
    """
    This function initializes and configures the FastAPI application.

    Parameters:
    None

    Returns:
    FastAPI: An instance of the FastAPI application with the following configurations:
             - Celery integration for asynchronous task processing.
             - HTTP request logging middleware.
             - Included router for handling review-related requests.
    """
    app = FastAPI()

    app.celery_app = create_celery()

    app.middleware('http')(log_requests)

    app.include_router(review_router)
    return app