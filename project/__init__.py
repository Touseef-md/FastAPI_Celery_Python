from fastapi import FastAPI
from project.celery_utils import create_celery   # new
from project.middlewares.logging_middleware import log_requests
from project.tasks import log_access
def create_app() -> FastAPI:
    app = FastAPI()

    # do this before loading routes              # new
    app.celery_app = create_celery()             # new
    
    # print("THis is the celery app: ", app.celery_app)
    # from project.users import users_router     # new
    # app.include_router(users_router)     
    
    app.middleware('http')(log_requests)

    from project.reviews import review_router
    app.include_router(review_router)                 # new
    

    @app.get("/")
    async def root():
        return {"message": "Hello World"}


    return app