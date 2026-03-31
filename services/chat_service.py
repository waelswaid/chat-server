from fastapi import WebSocket
from database import async_session
from connection_manager import manager
from repository.chat_repo import query_chats_for_existing_chat, insert_message, insert_new_chat, insert_users_to_chat_members
from models.chats import Chat
from models.chat_members import ChatMember
from models.messages import Message
import uuid

def generate_dm_key(sender_id:str, receiver_id:str):
    return min(sender_id, receiver_id) + ":" + max(sender_id, receiver_id)


# TODO error handling
# TODO move websocket call to send_personal_message() to chat_handler
async def chat_handler(msg_type:str, message:str,  sender_id:str, receiver_id:str):
    dm_key = generate_dm_key(sender_id, receiver_id)
    async with async_session() as session:
        chat_id = await query_chats_for_existing_chat(session, dm_key)
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
            return
        message_orm = Message(chat_id=chat_id, user_id = sender_id, message = message, type=msg_type)
        await insert_message(session, message_orm)
        await session.commit()
        return
