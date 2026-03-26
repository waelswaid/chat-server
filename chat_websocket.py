from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from connection_manager import manager
from schemas.message import Message
from core.auth_token import validate_token
from services.friend_service import request_handler

websocket_router = APIRouter()




@websocket_router.websocket("/ws/")
async def route_to_server(websocket: WebSocket):
    # extract token
    token = websocket.query_params.get("token")
    if not token:
        return
    try:
        # calidate and extract user_id, user_email
        user_id, user_email = validate_token(token)
    except Exception:
        await websocket.close(code=1008)
        return
    

    # connect user
    await manager.connect(websocket, user_id, user_email)
    # send online users list to user
    await websocket.send_json({
        "type": "user_list",
        "users": manager.get_online_users()
    })

    
    await manager.broadcast({"type": "user_joined", "user_id": user_id, "email": user_email})
    try:
        while True:
            # listen for incoming requests
            data = await websocket.receive_json()
            msg_type = data.get("type")


            if msg_type == "message":
                message = Message(**data)
                await manager.send_personal_message(message, user_email)
            else:
                await request_handler(msg_type,data,websocket,user_id)


    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.broadcast({"type": "user_left", "user_id": user_id, "email": user_email})