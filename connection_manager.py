from fastapi import WebSocket
from schemas.message import Message

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id:int):
        await websocket.accept()
        self.active_connections.update({client_id : websocket})

    def disconnect(self, websocket: WebSocket, client_id: int):
        del self.active_connections[client_id]

    async def send_personal_message(self, message: Message):
        to_websocket = self.active_connections.get(message.to)
        if to_websocket:
            await to_websocket.send_text(message.message)

    async def broadcast(self, message: str):
        ws_values = self.active_connections.values()
        for connection in ws_values:
            await connection.send_text(message)

    
manager = ConnectionManager()