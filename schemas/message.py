from pydantic import BaseModel




class Message(BaseModel):
    to: str
    message: str



class LoadHistory(BaseModel):
    chat_id: str
    before: int | None = None