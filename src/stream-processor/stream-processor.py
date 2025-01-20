import json

import redis
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, from_json, struct, to_json
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

message_schema = StructType(
    [
        StructField("timestamp", StringType(), True),
        StructField("message", StringType(), True),
        StructField("id", IntegerType(), True),
    ]
)

spark = SparkSession.builder.appName("StreamProcessor").getOrCreate()

redis_pool = redis.ConnectionPool(host="redis", port=6379, db=0)


def write_to_redis_and_kafka(df, epoch_id):
    r = redis.Redis(connection_pool=redis_pool)

    notification_df = df.select(
        to_json(
            struct(lit("notification").alias("type"), col("id").alias("from"))
        ).alias("value")
    )

    notification_df.write.format("kafka").option(
        "kafka.bootstrap.servers", "kafka-1.kafka-headless:9092"
    ).option("topic", "notifications").save()

    rows = df.collect()
    for row in rows:
        message_data = {
            "timestamp": row["timestamp"],
            "message": row["message"],
            "id": row["id"],
        }
        r.rpush("notification", json.dumps(message_data))


df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-0.kafka-headless:9092")
    .option("subscribe", "test-topic")
    .option("startingOffsets", "latest")
    .load()
)

parsed_df = df.select(
    from_json(col("value").cast("string"), message_schema).alias("parsed_value")
).select("parsed_value.*")

query = (
    parsed_df.writeStream.foreachBatch(write_to_redis_and_kafka)
    .outputMode("append")
    .start()
)

query.awaitTermination()
