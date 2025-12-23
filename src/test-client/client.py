import asyncio
import json
from datetime import datetime

import websockets


async def connect_to_websockets():
    endpoints = [
        "ws://backend.local/ws/stock-indicators",
        "ws://backend.local/ws/notifications",
    ]

    async def handle_websocket(uri):
        try:
            async with websockets.connect(uri) as websocket:
                print(f"Connected to {uri}")

                while True:
                    try:
                        message = await websocket.recv()
                        parsed_message = json.loads(message)
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        if uri.endswith("/ws/notifications"):
                            signal = parsed_message.get("signal", "Unknown Signal")
                            print(f"[{current_time}] Signal: {signal}")

                        elif uri.endswith("/ws/stock-indicators"):
                            stock_data = {
                                "timestamp": parsed_message.get("timestamp"),
                                "open": parsed_message.get("open"),
                                "high": parsed_message.get("high"),
                                "low": parsed_message.get("low"),
                                "close": parsed_message.get("close"),
                                "volume": parsed_message.get("volume"),
                                "moving_average": parsed_message.get("moving_average"),
                                "ema": parsed_message.get("ema"),
                                "rsi": parsed_message.get("rsi"),
                            }

                            print(f"[{current_time}] Stock Indicators:")
                            for key, value in stock_data.items():
                                print(f"  {key}: {value}")
                            print("-" * 40)

                    except websockets.ConnectionClosed:
                        print(f"Connection closed: {uri}")
                        break

        except Exception as e:
            print(f"Error connecting to {uri}: {e}")

    await asyncio.gather(*[handle_websocket(endpoint) for endpoint in endpoints])


async def main():
    await connect_to_websockets()


if __name__ == "__main__":
    asyncio.run(main())
