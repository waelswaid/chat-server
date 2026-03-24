from fastapi import APIRouter, WebSocket
from connection_manager import manager


websocket_router = APIRouter()



@websocket_router.websocket("/ws/{client_id}")
async def route_to_server(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            recipient_id = data["to"]
            message = data["message"]
            pass
    except:
        pass