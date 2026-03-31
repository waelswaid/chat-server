from database import async_session
from repository.chat_repo import (
    query_chats_for_existing_chat, insert_message, insert_new_chat, insert_users_to_chat_members,
    load_messages, is_chat_member)
from models.chats import Chat
from models.chat_members import ChatMember
from models.messages import Message
import uuid
from sqlalchemy.exc import SQLAlchemyError


def generate_dm_key(sender_id:str, receiver_id:str):
    return min(sender_id, receiver_id) + ":" + max(sender_id, receiver_id)


async def chat_handler(msg_type:str, message:str,  sender_id:str, receiver_id:str):
    dm_key = generate_dm_key(sender_id, receiver_id)
    async with async_session() as session:
        try:
            chat_id = await query_chats_for_existing_chat(session, dm_key)
            # no chat_id means no existing chat between two users
            if not chat_id:
                chat_id = str(uuid.uuid4())
                chat = Chat(chat_id=chat_id, chat_name=None, is_group=False, dm_key=dm_key)
                member1 = ChatMember(chat_id = chat_id, user_id = sender_id, is_admin=False)
                member2 = ChatMember(chat_id = chat_id, user_id = receiver_id, is_admin=False)
                await insert_new_chat(session, chat)
                await insert_users_to_chat_members(session, member1, member2)

            message_orm = Message(chat_id=chat_id, user_id = sender_id, message = message, type=msg_type)
            await insert_message(session, message_orm)
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise



async def load_chat(chat_id: str, before_message_id:int|None, user_id:str):
    async with async_session() as session:
        result = await is_chat_member(session, chat_id, user_id)
        if not result:
            return {"type": "message_error", "message": "unauthorized chat"}
        messages =  await load_messages(session, chat_id, before_message_id)   
            
        # load_messages() returns a list of Message ORM instances, I need to convert to dicts/json b4 returning to the websocket
        return {"type": "load_history", "messages": [
            {"message_id": m.message_id, "user_id": m.user_id, "message": m.message, "type": m.type, "timestamp": str(m.timestamp)}
            for m in reversed(messages)]}