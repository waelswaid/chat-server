import asyncio
import websockets
import json


async def client(client_id):
    uri = f"ws://localhost:8000/server/ws/{client_id}"
    async with websockets.connect(uri) as ws:
        async def listen():
            while True:
                msg = await ws.recv()
                print(f"recieved: {msg}")
        
        listen_task = asyncio.create_task(listen())

        while True:
            text = await asyncio.get_event_loop().run_in_executor(None, input, "message:")
            to, message = text.split(":", 1)
            await ws.send(json.dumps({"to": int(to), "message": message}))


asyncio.run(client(1))