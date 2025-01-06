from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def create_spark_session():
    return SparkSession.builder.appName("KafkaConsumer").getOrCreate()


def process_stream():
    spark = create_spark_session()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-0.kafka-headless:9092")
        .option("subscribe", "test-topic")
        .load()
    )

    messages = df.selectExpr("CAST(value AS STRING)")

    query = (
        messages.writeStream.outputMode("append")
        .format("text")
        .option("path", "/app/output")
        .option("checkpointLocation", "/app/checkpoint")
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    process_stream()
