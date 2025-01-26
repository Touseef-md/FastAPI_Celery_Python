# tasks.py
# from main import app
from celery import current_app as current_celery_app
from celery import shared_task
from project.reviews.models import AccessLog
from project.database import SessionLocal
import time
# print("task.py called")
@shared_task
def log_access(log_entry: str):
    db = SessionLocal()
    access_log = AccessLog()
    access_log.text = log_entry
    db.add(access_log)
    db.commit()
    db.close()
    time.sleep(10)
