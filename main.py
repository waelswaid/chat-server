from fastapi import FastAPI
from routes.chat_websocket import websocket_router
from routes.upload_route import upload_router
from contextlib import asynccontextmanager
from database import engine




@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan = lifespan)



@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(websocket_router, prefix="/server")
app.include_router(upload_router, prefix="/server")


