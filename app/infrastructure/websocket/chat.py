from fastapi import APIRouter
from starlette.websockets import WebSocket


chat_router = APIRouter()


@chat_router.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"Echo kaiba: {message}")
