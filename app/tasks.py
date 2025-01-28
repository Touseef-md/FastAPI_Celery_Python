from celery import shared_task
from app.reviews.models import AccessLog
from app.database import SessionLocal

@shared_task
def log_access(log_entry: str) -> None:
    """
    This function logs access details to the database using Celery task.

    Parameters:
    log_entry (str): The access log entry to be stored in the database.

    Returns:
    None: This function does not return any value. It logs the access details to the database.
    """
    db = SessionLocal()
    access_log = AccessLog()
    access_log.text = log_entry
    db.add(access_log)
    db.commit()
    db.close()