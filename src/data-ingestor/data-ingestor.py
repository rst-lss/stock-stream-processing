import json
import os
import time
from datetime import datetime

from kafka import KafkaProducer


def create_producer():
    return KafkaProducer(
        bootstrap_servers=[
            os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka-0.kafka-headless:9092")
        ],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_message():
    producer = create_producer()

    while True:
        try:
            message = {
                "timestamp": datetime.now().isoformat(),
                "message": "Hello from Python Producer!",
                "id": int(time.time()),
            }

            future = producer.send(
                topic=os.getenv("KAFKA_TOPIC", "test-topic"), value=message
            )

            record_metadata = future.get(timeout=10)
            print(
                f"Message sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}"
            )

            time.sleep(float(os.getenv("MESSAGE_INTERVAL", "5")))

        except Exception as e:
            print(f"Error producing message: {str(e)}")
            time.sleep(5)


if __name__ == "__main__":
    send_message()
