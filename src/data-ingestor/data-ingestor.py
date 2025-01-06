import json

from kafka import KafkaProducer


def create_producer():
    return KafkaProducer(
        bootstrap_servers=["kafka-0.kafka-headless:9092"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )


def send_message():
    producer = create_producer()
    message = {"message": "Hello from Python!"}
    producer.send("test-topic", message)

    producer.flush()
    producer.close()


if __name__ == "__main__":
    send_message()
