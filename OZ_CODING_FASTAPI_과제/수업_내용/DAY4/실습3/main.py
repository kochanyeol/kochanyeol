from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import psutil
import random
app = FastAPI()

@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept() # WebSocket 연결 수락 = 연결하면 실행
    secret_number = random.randint(1, 100)
    attemps = 0
    await websocket.send_text("GAME START")

    try:
        while True:
            data = await websocket.receive_text() # 클라이언트 -> 서버
            guess = int(data)
            attemps += 1
            if guess < secret_number:
                await websocket.send_text("UP")
            if guess > secret_number:
                await websocket.send_text("DOWN")
            else:
                await websocket.send_text(f"성공 {attemps}")
                break

            await websocket.send_text(f"서버 응답: {data}") # 서버 -> 클라이언트
    except WebSocketDisconnect:
        print("연결 해제")
        await websocket.close()