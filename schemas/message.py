from pydantic import BaseModel

class Message(BaseModel):
    to: int
    message: str