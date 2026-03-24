from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connection_manager import manager
from schemas.message import Message

websocket_router = APIRouter()



@websocket_router.websocket("/ws/{client_id}")
async def route_to_server(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    await manager.broadcast(f"user {client_id} has joined the chat.")
    try:
        while True:
            data = await websocket.receive_json()
            message = Message(**data)
            await manager.send_personal_message(message)

    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast(f"user {client_id} has left the chat.")