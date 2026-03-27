from schemas.friend_request import FriendRequest, FriendAccept,FriendDecline, FriendRemove
from fastapi import WebSocket
from database import async_session
from repository.friend_system_repo import (
    send_friend_req_to_db, friend_request_accept_to_db,
    friend_req_decline_to_db, friend_remove_from_db
) 
from sqlalchemy.exc import IntegrityError
from connection_manager import manager



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
    


async def friend_request_accept(req : FriendAccept, websocket:WebSocket, accepter_id: str) -> None:
    requester_id = req.from_user
    async with async_session() as session:
        try:
            await friend_request_accept_to_db(session, requester_id, accepter_id)
        except (IntegrityError, ValueError):
            await session.rollback()
            await websocket.send_json({"type":"friend_req_accept_error", "message":"invalid request"})
            return
        await websocket.send_json({"type": "friend_req_accepted", "from": req.from_user})
        return
    

async def friend_request_declined(req : FriendDecline, websocket:WebSocket, decliner_id: str) -> None:
    requester_id = req.from_user
    async with async_session() as session:
        try:
            await friend_req_decline_to_db(session, requester_id, decliner_id)
        except(IntegrityError, ValueError):
            await session.rollback()
            await websocket.send_json({"type":"friend_req_decline_error", "message":"invalid request"})
            return
        await websocket.send_json({"type": "friend_req_declined", "from": req.from_user})
        return
        
async def friend_remove(req: FriendRemove, websocket : WebSocket, remover_id: str):
    removed_id = req.user_id
    async with async_session() as session:
        try:
            await friend_remove_from_db(session, removed_id,remover_id)
        except (IntegrityError, ValueError):
            await session.rollback()
            await websocket.send_json({"type":"friend_remove_error", "message":"invalid request"})
            return
        await websocket.send_json({"type": "friend_remove", "from": req.user_id})
        return
        

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
        await friend_request_accept(req,websocket,user_id)
    elif msg_type == "friend_decline":
        req = FriendDecline(**data)
        await friend_request_declined(req,websocket,user_id)
    elif msg_type == "friend_remove":
        req = FriendRemove(**data)
    elif msg_type == "friend_list":
        await return_friend_list(websocket)
    elif msg_type == "pending_list":
        await return_pending_list(websocket)
    else:
        await websocket.send_json({"type": "error", "message": "unknown type"})