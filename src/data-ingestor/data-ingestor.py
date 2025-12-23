import json
import os
import time
from datetime import datetime, timedelta

import requests
from kafka import KafkaProducer

API_KEY = os.getenv("API_KEY", "bh_3QSqE2TN3MbwPE87XuC0df12C_8Ss")
STOCK_SYMBOL = os.getenv("STOCK_SYMBOL", "AAPL")
MULTIPLIER = os.getenv("MULTIPLIER", "60")
TIMESPAN = os.getenv("TIMESPAN", "minute")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-0.kafka-headless:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "stock_data")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 30))
START_DATE = datetime(2024, 1, 1)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def fetch_stock_data(for_date):
    # Calculate end date as last day of the month
    next_month = for_date.replace(day=28) + timedelta(days=4)  # Go to next month
    end_date = next_month - timedelta(days=next_month.day)  # Last day of current month

    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{STOCK_SYMBOL}/range/{int(MULTIPLIER)}/{TIMESPAN}/"
        f"{for_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}?"
        f"adjusted=true&sort=asc&apiKey={API_KEY}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            stock_data = {}
            for bar in data["results"]:
                # Convert ms timestamp to 'YYYY-MM-DD HH:MM:SS' format
                timestamp = datetime.fromtimestamp(bar["t"] / 1000).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                stock_data[timestamp] = {
                    "open": float(bar["o"]),
                    "high": float(bar["h"]),
                    "low": float(bar["l"]),
                    "close": float(bar["c"]),
                    "volume": int(bar["v"]),
                }

            return stock_data

        else:
            print("Error: Unexpected response format", data)
            return None
    else:
        print(f"Error: Failed to fetch data (status code {response.status_code})")
        return None


def produce_messages():
    current_date = START_DATE

    while True:
        print(f"Fetching data for {current_date.strftime('%Y-%m')}...")
        stock_data = fetch_stock_data(current_date)

        if stock_data:
            for timestamp in sorted(stock_data.keys()):
                values = stock_data[timestamp]
                message = {
                    "timestamp": timestamp,
                    "open": values["open"],
                    "high": values["high"],
                    "low": values["low"],
                    "close": values["close"],
                    "volume": values["volume"],
                }
                print(f"Sending message: {message}")
                producer.send(KAFKA_TOPIC, message)

        current_date += timedelta(days=31)
        current_date = current_date.replace(day=1)

        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    try:
        produce_messages()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        producer.close()
