from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket]

    async def connect(self, websocket: WebSocket, client_id:int):
        await websocket.accept()
        self.active_connections.update({client_id : websocket})

    def disconnect(self, websocket: WebSocket, client_id: int):
        del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: int):
        websocket = self.active_connections.pop(client_id)
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        ws_values = self.active_connections.values()
        for connection in ws_values:
            await connection.send_text(message)

    
manager = ConnectionManager()