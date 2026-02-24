from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws/monitor")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # WebSocket 연결 수락 = 연결하면 실행
    try:
        while True:
            data = await websocket.receive_text() # 클라이언트 -> 서버
            await websocket.send_text(f"서버 응답: {data}") # 서버 -> 클라이언트
    except WebSocketDisconnect:
        print("연결 해제")
        await websocket.close()