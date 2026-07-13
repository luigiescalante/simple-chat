import json

from fastapi import APIRouter
from starlette.websockets import WebSocket

from app.service.chat import IAChatService

chat_router = APIRouter()


@chat_router.websocket("/ws/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    chat_srv = IAChatService()
    chat_srv.new_chat()
    await websocket.send_text(chat_srv.start_conversation())
    while True:
        response_plane_text = await websocket.receive_text()
        response = json.loads(response_plane_text)
        msg = response["msg"]
        if chat_srv.chat.exit_message(msg):
            await websocket.close(1000, reason="Finished conversation")
            return
        response = chat_srv.send_message(msg)
        ia_response = chat_srv.chat.ia_response(str(response))
        response_ws = json.dumps(ia_response)
        await websocket.send_text(response_ws)
