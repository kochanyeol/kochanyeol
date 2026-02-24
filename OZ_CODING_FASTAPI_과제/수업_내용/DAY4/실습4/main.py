from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/{nickname}")
async def websocket_endpoint(websocket:WebSocket, nickname: str):
    await websocket.accept()
    await websocket.send_text(f'{nickname}님 환영')
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"{nickname}님 메세지 : {data}")

    except WebSocketDisconnect:
        print("연결 해제")
        await websocket.close()