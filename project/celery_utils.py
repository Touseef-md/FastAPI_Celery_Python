from celery import current_app as current_celery_app

from project.config import settings


def create_celery():
    print("Create celery called")
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")
    celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    )   
    # print("Celery confi is: ", celery_app.conf)

    return celery_app