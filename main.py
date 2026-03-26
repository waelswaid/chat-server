from fastapi import FastAPI
from chat_websocket import websocket_router


app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(websocket_router, prefix="/server")



