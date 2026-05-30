import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from connections import ConnectionManager
from database import create_message, init_db, list_messages


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()


@app.on_event("startup")
async def startup() -> None:
    init_db()


@app.get("/")
async def dashboard():
    return {"status": "fastapi websocket server running"}


@app.get("/messages")
async def messages(limit: int = 100):
    return {"messages": list_messages(limit)}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        await manager.send_message(websocket, "connected to websocket server")
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                sender = payload["sender"].strip()
                content = payload["content"].strip()
            except (json.JSONDecodeError, KeyError, AttributeError):
                await manager.send_message(
                    websocket,
                    "message must be JSON with sender and content fields",
                )
                continue

            if not sender or not content:
                await manager.send_message(
                    websocket,
                    "sender and content are required",
                )
                continue

            saved_message = create_message(
                sender=sender,
                content=content,
            )

            await manager.broadcast(json.dumps(saved_message))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("a client has disconnected")
