from schemas.friend_request import FriendRequest, FriendAccept,FriendDecline, FriendRemove
from fastapi import WebSocket
from database import async_session
from repository.friend_system_repo import send_friend_req_to_db
from sqlalchemy.exc import IntegrityError
from connection_manager import manager
from models.pending_requests import PendingRequests



async def send_friend_request(req : FriendRequest, websocket:WebSocket, user_id: str) -> None:
    to = req.to
    sender_id = user_id
    async with async_session() as session:
        try:
            await send_friend_req_to_db(session,to,sender_id)
        except IntegrityError:
            await session.rollback()
            await websocket.send_json({"type":"send_friend_req_error", "message":"invalid request"})
            return
    await websocket.send_json({"type": "friend_request_sent", "to": req.to})
    return
    


async def friend_request_accept(req : FriendAccept, websocket:WebSocket, user_id: str):
    pass

async def friend_request_declined(req : FriendDecline, websocket:WebSocket, user_id: str):
    pass

async def return_friend_list(websocket:WebSocket):
    pass

async def return_pending_list(websocket:WebSocket):
    pass



async def request_handler(msg_type:str, data:dict, websocket:WebSocket, user_id:str):
    if msg_type == "friend_request":
        req = FriendRequest(**data)
        await send_friend_request(req, websocket, user_id)
    elif msg_type == "friend_accept":
        req = FriendAccept(**data)
        pass
    elif msg_type == "friend_decline":
        req = FriendDecline(**data)
        pass
    elif msg_type == "friend_list":
        pass
    elif msg_type == "pending_list":
        pass
    else:
        await websocket.send_json({"type": "error", "message": "unknown type"})