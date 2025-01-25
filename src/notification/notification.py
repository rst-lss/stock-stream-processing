import asyncio
from typing import List

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


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


@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


async def consume_kafka_messages():
    consumer = AIOKafkaConsumer(
        "trading_signals",
        bootstrap_servers="kafka-1.kafka-headless:9092",
        auto_offset_reset="latest",
    )

    await consumer.start()

    try:
        async for message in consumer:
            try:
                decoded_message = message.value.decode("utf-8")
                await connection_manager.broadcast(decoded_message)
            except Exception as e:
                print(f"Error processing message: {e}")
    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_kafka_messages())


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
