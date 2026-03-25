from pydantic import BaseModel

class Message(BaseModel):
    to: str
    message: str