from fastapi import WebSocket
from schemas.message import Message

class ConnectionManager:
    # active connections pool
    def __init__(self):
        self.active_connections: dict[str, dict] = {}        

    async def connect(self, websocket: WebSocket, user_id: str, user_email : str):
        await websocket.accept()
        self.active_connections.update({user_id : {"websocket" : websocket, "email" : user_email}})

    def disconnect(self, websocket: WebSocket, user_id: str):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: Message, user_email: str):
        # active_connections --> {user_id : {"websocket":websocket, "email" : user_email}}
        inner = self.active_connections.get(message.to) # inner = {"websocket":websocket, "email":user_email}
        if inner:
            to_websocket = inner["websocket"] # to_websocket = websocket
            await to_websocket.send_json({"type":"message", "from":user_email, "message":message.message })

    async def broadcast(self, message: dict):
        for inner in self.active_connections.values():
            await inner["websocket"].send_json(message)

    def get_online_users(self) -> list[dict]:
        return [
            {"user_id": uid, "email": inner["email"]}
            for uid, inner in self.active_connections.items()
            # .items()-> list[tuples] = [(uid:{"websocket":websocket,"email":email}),(),...] 
        ]
                            
    
manager = ConnectionManager()