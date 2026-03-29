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


    # email is the human readable display name for the "from" field, and user_id is the internal lookup key for routing 
    async def send_personal_message(self,msg_type:str, to: str, message: str, sender_email: str):
        # active_connections --> {user_id : {"websocket":websocket, "email" : user_email}}
        inner = self.active_connections.get(to) # inner = {"websocket":websocket, "email":user_email}
        if inner:
            to_websocket = inner["websocket"] # to_websocket = websocket
            await to_websocket.send_json({"type":msg_type, "from":sender_email, "message":message })

    async def broadcast(self, message: dict):
        for inner in self.active_connections.values():
            await inner["websocket"].send_json(message)

    def get_connection(self, user_id: str) -> WebSocket | None:
        inner = self.active_connections.get(user_id)
        if inner:
            return inner["websocket"]
        return None

    def get_email(self, user_id: str) -> str | None:
        inner = self.active_connections.get(user_id)
        if inner:
            return inner["email"]
        return None

    def get_online_users(self) -> list[dict]:
        return [
            {"user_id": uid, "email": inner["email"]}
            for uid, inner in self.active_connections.items()
            # .items()-> list[tuples] = [(uid:{"websocket":websocket,"email":email}),(),...] 
        ]
                            
    
manager = ConnectionManager()