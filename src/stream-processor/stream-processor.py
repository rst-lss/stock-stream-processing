import redis
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("StreamProcessor").getOrCreate()

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-0.kafka-headless:9092")
    .option("subscribe", "test-topic")
    .option("startingOffsets", "latest")
    .load()
)

df_string = df.selectExpr("CAST(value AS STRING)")

query = (
    df_string.writeStream.outputMode("append")
    .format("console")
    .option("truncate", False)
    .start()
)

query.awaitTermination()
