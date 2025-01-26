from fastapi import APIRouter

users_router = APIRouter(
    prefix="/users",
)

@users_router.get("/")
async def get_users():
    # Logic to retrieve users
    return {"message": "List of users"}

from . import models, tasks # noqa