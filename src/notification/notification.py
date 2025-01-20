import json
import socket

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

spark = SparkSession.builder.appName("NotificationProcessor").getOrCreate()

notification_schema = StructType(
    [StructField("type", StringType(), True), StructField("from", IntegerType(), True)]
)


def process_batch(df, epoch_id):
    messages = df.collect()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("backend-service", 5000))

    for msg in messages:
        socket_message = {"type": msg.type, "from": msg.from_}
        client_socket.send(json.dumps(socket_message).encode())

    client_socket.close()


df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-1.kafka-headless:9092")
    .option("subscribe", "notifications")
    .option("startingOffsets", "latest")
    .load()
)

query = (
    df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), notification_schema).alias("data"))
    .select("data.*")
    .writeStream.foreachBatch(process_batch)
    .outputMode("append")
    .start()
)

query.awaitTermination()
