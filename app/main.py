import logging
from os import environ

import uvicorn
from fastapi import FastAPI, APIRouter

from app.infrastructure.handler.healthy import healthy_api_router
from app.infrastructure.websocket.chat import chat_router

API_V1_PREFIX = "/api/v1"
app = FastAPI()

# api path
api_v1 = APIRouter(prefix=API_V1_PREFIX)
api_v1.include_router(healthy_api_router)  # healthy
app.include_router(api_v1)
# websocket path
app.include_router(chat_router)  # chat


def start_server() -> Exception | None:
    host = environ.get("HOST")
    if host is None:
        raise Exception("No host provided")
    port = environ.get("PORT")
    if port is None:
        raise Exception("No port provided")

    uvicorn.run(
        "app.main:app",
        host=host,
        port=int(port),
        reload=True,
    )


def main():
    try:
        start_server()
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    main()
