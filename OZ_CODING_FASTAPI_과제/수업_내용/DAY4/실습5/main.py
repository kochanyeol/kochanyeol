from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
jinja2
app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for conn in self.active_connections:
            await conn.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/chat/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await manager.connect(websocket)

    await manager.broadcast(
        {
            "type" : "system",
            "message" : f"{client_name}님 입장"
        }
    )

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(
                {
                    "type" : "chat",
                    "message" : data,
                    "sender" : client_name
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            {
                "type" : "system",
                "message" : f"{client_name}님 퇴장"
            }
        )