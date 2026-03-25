from fastapi import WebSocket
from schemas.message import Message

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, user_id: str, user_email : str):
        await websocket.accept()
        self.active_connections.update({user_id : {"websocket" : websocket, "email" : user_email}})

    def disconnect(self, websocket: WebSocket, user_id: str):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: Message):
        inner = self.active_connections.get(message.to)
        if inner:
            to_websocket = inner["websocket"]
            await to_websocket.send_text(message.message) # TODO send_json with structured data {"type": "message", "from": sender_id, "message": "..."}

    async def broadcast(self, message: dict):
        for inner in self.active_connections.values():
            await inner["websocket"].send_json(message)

    
manager = ConnectionManager()