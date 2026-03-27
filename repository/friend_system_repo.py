from models.friendships import Friendships
from models.pending_requests import PendingRequests
from schemas.friend_request import FriendRequest, FriendAccept,FriendDecline, FriendRemove
from database import async_session
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete, or_, and_

async def send_friend_req_to_db(session, to:str, user_id: str) -> None:
    request = PendingRequests(
        sender_id = user_id,
        receiver_id = to
    )
    session.add(request)
    await session.commit()    
    return

# delete from PendingRequests, insert into Friendships (single transaction)
async def friend_request_accept_to_db(session, requester_id:str, accepter_id:str) -> None:
    result = await session.execute(
        delete(PendingRequests).where(
            PendingRequests.sender_id == requester_id,
            PendingRequests.receiver_id == accepter_id
        )
    )
    if result.rowcount == 0:
        raise ValueError("no pending request found")
    
    session.add_all([
        Friendships(user_id=accepter_id, friend_id=requester_id),
        Friendships(user_id = requester_id, friend_id=accepter_id)
    ])
    await session.commit()
    return
        

async def friend_req_decline_to_db(session, requester_id: str, decliner_id:str) -> None:
    result = await session.execute(
        delete(PendingRequests).where(
            PendingRequests.sender_id == requester_id,
            PendingRequests.receiver_id == decliner_id
        )
    )
    if result.rowcount == 0:
        raise ValueError("no pending request found")
    await session.commit()
    return

async def friend_remove_from_db(session, removed_id: str, remover_id:str) -> None:
    result = await session.execute(
        delete(Friendships).where(
            or_(
                and_(Friendships.user_id == remover_id, Friendships.friend_id == removed_id),
                and_(Friendships.user_id == removed_id, Friendships.friend_id == remover_id)
            )

        )
    )
    if result.rowcount == 0:
        raise ValueError("not friends")
    await session.commit()
    return