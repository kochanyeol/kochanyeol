import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import psutil # 컴퓨터 정보 불러오기
import asyncio

app = FastAPI()

@app.websocket("/ws/monitor")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    try:
        while True:

            data = {
                "cpu": psutil.cpu_percent(),
                "ram": psutil.virtual_memory().percent()
            }
            await websocket.send_json(data)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("연결 해제")
        await websocket.close()