from celery import current_app as current_celery_app
from app.config import settings


def create_celery():
    """
    This function creates and configures a Celery application instance.

    Parameters:
    None

    Returns:
    celery_app: A configured Celery application instance.

    The function initializes a Celery application using the current_celery_app from the celery module.
    It then configures the Celery application using the settings module and updates its configuration with
    specific settings such as task_serializer, accept_content, result_serializer, timezone, and enable_utc.
    Finally, it returns the configured Celery application instance.
    """

    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )   

    return celery_app
