import json
import os
import time
from datetime import datetime, timedelta

import requests
from kafka import KafkaProducer

API_KEY = os.getenv("API_KEY", "DEMO_KEY")
STOCK_SYMBOL = os.getenv("STOCK_SYMBOL", "AAPL")
DATA_INTERVAL = os.getenv("DATA_INTERVAL", "60min")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka-0.kafka-headless:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "stock_data")
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 60))
START_DATE = datetime(2009, 2, 1)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def fetch_stock_data(for_date):
    url = (
        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_SYMBOL}"
        f"&interval={DATA_INTERVAL}&month={for_date.year - 2008}-{for_date.month:02d}&apikey={API_KEY}"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "Time Series (60min)" in data:
            return data["Time Series (60min)"]
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
                    "open": float(values["1. open"]),
                    "high": float(values["2. high"]),
                    "low": float(values["3. low"]),
                    "close": float(values["4. close"]),
                    "volume": int(values["5. volume"]),
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
