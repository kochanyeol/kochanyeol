from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def get_async_items():
    await asyncio.sleep(1)
    return {"hello": "world"}