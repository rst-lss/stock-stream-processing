import json
import os
import time

import requests
from kafka import KafkaProducer


def create_producer():
    return KafkaProducer(
        bootstrap_servers=[
            os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-0.kafka-headless:9092")
        ],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def get_bitcoin_price(api_url="https://api.coindesk.com/v1/bpi/currentprice.json"):
    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        current_price = data["bpi"]["USD"]["rate"]
        return {"price_usd": current_price}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return {"error": str(e)}


if __name__ == "__main__":

    producer = create_producer()

    while True:
        bitcoin_price = get_bitcoin_price()

        if "price_usd" in bitcoin_price:
            producer.send(
                topic=os.getenv("KAFKA_TOPIC", "bitcoin_prices"), value=bitcoin_price
            )

        else:
            print(f"Error: {bitcoin_price['error']}")
        time.sleep(1)
