import asyncio
from typing import List

import aioredis
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class StockIndicator(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    moving_average: float
    ema: float
    rsi: float


app = FastAPI()
REDIS_URL = "redis://redis:6379/0"
STOCK_INDICATORS_KEY = "stock_indicators"


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


connection_manager = ConnectionManager()


@app.websocket("/ws/stock-indicators")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


async def watch_redis_key():
    redis = await aioredis.from_url(REDIS_URL)
    previous_length = 0

    while True:
        try:
            current_length = await redis.llen(STOCK_INDICATORS_KEY)

            if current_length >= previous_length + 5:
                new_items = await redis.lrange(
                    STOCK_INDICATORS_KEY, previous_length, current_length - 1
                )

                for item in new_items:
                    await connection_manager.broadcast(item.decode("utf-8"))

                previous_length = current_length

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Error watching Redis key: {e}")
            await asyncio.sleep(5)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(watch_redis_key())


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
