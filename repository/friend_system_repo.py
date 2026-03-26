from models.friendships import Friendships
from models.pending_requests import PendingRequests
from schemas.friend_request import FriendRequest, FriendAccept,FriendDecline, FriendRemove
from database import async_session
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError

async def send_friend_req_to_db(session, to:str, user_id: str) -> None:
    request = PendingRequests(
        sender_id = user_id,
        receiver_id = to
    )
    session.add(request)
    await session.commit()    
    return