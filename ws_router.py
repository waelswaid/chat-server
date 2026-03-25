from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connection_manager import manager
from schemas.message import Message
from core.auth_token import validate_token

websocket_router = APIRouter()



@websocket_router.websocket("/ws/")
async def route_to_server(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        return
    try:
        user_id, user_email = validate_token(token)
    except Exception:
        await websocket.close(code=1008)
        return
    await manager.connect(websocket, user_id, user_email)
    await websocket.send_json({
        "type": "users_list",
        "users": manager.get_online_users()
    })
    await manager.broadcast({"type": "user_joined", "user_id": user_id, "email": user_email})
    try:
        while True:
            data = await websocket.receive_json()
            message = Message(**data)
            await manager.send_personal_message(message, user_email)

    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast({"type": "user_left", "user_id": user_id, "email": user_email})