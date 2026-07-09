import datetime

from fastapi import APIRouter

healthy_api_router = APIRouter()


@healthy_api_router.get("/healthy")
async def healthy():
    return {
        "healthy": True,
        "date": datetime.datetime.now(),
    }
