# Notification Service Code Explanation

## WebSocket Connection Management (`ConnectionManager`)
```python
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
```
The `ConnectionManager` class handles WebSocket connections for real-time notifications:
- **Active Connections**: Maintains a list of all active WebSocket connections.
- **Connect**: Adds a new WebSocket connection to the list and accepts it.
- **Disconnect**: Removes a WebSocket connection from the list.
- **Broadcast**: Sends a message to all active WebSocket connections.


## WebSocket Endpoint 
```python
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
```
Defines a WebSocket route to handle client connections:
- Connects the WebSocket using `ConnectionManager`.
- Listens for incoming messages in a loop.
- Handles disconnections gracefully with `WebSocketDisconnect`.


## Kafka Consumer for Trading Signals
```python
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
```
Consumes messages from the `trading_signals` Kafka topic and broadcasts them to active WebSocket connections:
- Uses `AIOKafkaConsumer` to connect to the Kafka broker.
- Processes incoming messages asynchronously.
- Broadcasts decoded messages to all WebSocket clients via `ConnectionManager`.
- Stops the consumer gracefully on shutdown.


## Application Startup Event (`startup_event`)
```python
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_kafka_messages())
```
Automatically starts the Kafka consumer task when the application starts.


## Health Check Endpoint (`/health`)
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```
Provides a simple health check endpoint to verify if the application is running.


## Main Entry Point
```python
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
```

Starts the FastAPI application using Uvicorn, running on `0.0.0.0:5000`.
