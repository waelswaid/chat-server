from database import async_session
from sqlalchemy import delete, or_, and_, select
from models.chats import Chat
from models.chat_members import ChatMember
from models.messages import Message


async def query_chats_for_existing_chat(session, dm_key:str) -> str | None:
    # select chat_id from chats where dm_key = dm_key
    result = (await session.execute(
        select(Chat.chat_id).where(Chat.dm_key == dm_key)
    )).scalars().first()
    return result

# chat: chat_name, created_at, is_group, dm_key
async def insert_new_chat(session, chat: Chat):
    session.add(chat)

async def insert_users_to_chat_members(session, user1:ChatMember, user2:ChatMember):
    session.add(user1)
    session.add(user2)

async def insert_message(session, message:Message):
    session.add(message)


async def load_messages(session, chat_id:str, before_message_id:int|None):
    query = select(Message).where(Message.chat_id == chat_id)
    if before_message_id is not None:
        query = query.where(Message.message_id <= before_message_id)                 
    query = query.order_by(Message.message_id.desc()).limit(10)
    return (await session.execute(query)).scalars().all()


async def is_chat_member(session, chat_id: str, user_id: str) -> bool:
    result = (await session.execute(    
        select(ChatMember.user_id)
        .where(ChatMember.chat_id == chat_id, ChatMember.user_id == user_id)                                                                 )).scalars().first()
    return result is not None 