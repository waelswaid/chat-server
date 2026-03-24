from fastapi import FastAPI
from ws_router import websocket_router



app = FastAPI()



app.include_router(websocket_router, prefix="/server")



