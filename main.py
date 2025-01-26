from celery import Celery
# from fastapi import FastAPI

# app = FastAPI()

# celery = Celery(
#     __name__,
#     broker="redis://127.0.0.1:6379/0",
#     backend="redis://127.0.0.1:6379/0"
# )

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @celery.task
# def divide(x, y):
#     import time
#     time.sleep(5)
#     return x / y


from project import create_app
print("This is the main")
print(__name__)
app = create_app()
celery = app.celery_app
# app.celery_app = celery