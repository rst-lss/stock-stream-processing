from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, struct, to_json, when
from pyspark.sql.types import FloatType, StringType, StructField, StructType


def generate_signals(parsed_stream):
    return parsed_stream.withColumn(
        "signal",
        when((col("rsi") < 30) & (col("close") < col("ema")), "buy")
        .when((col("rsi") > 70) & (col("close") > col("ema")), "sell")
        .otherwise("hold"),
    )


def process_kafka_messages(spark):
    schema = StructType(
        [
            StructField("timestamp", StringType(), True),
            StructField("open", FloatType(), True),
            StructField("high", FloatType(), True),
            StructField("low", FloatType(), True),
            StructField("close", FloatType(), True),
            StructField("volume", FloatType(), True),
            StructField("moving_average", FloatType(), True),
            StructField("ema", FloatType(), True),
            StructField("rsi", FloatType(), True),
        ]
    )

    raw_stream = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-1.kafka-headless:9092")
        .option("subscribe", "stock_indicators")
        .option("startingOffsets", "latest")
        .load()
    )

    parsed_stream = raw_stream.select(
        from_json(col("value").cast("string"), schema).alias("data")
    ).select("data.*")

    trading_signals = generate_signals(parsed_stream)

    output_stream = trading_signals.select(
        to_json(
            struct(
                col("timestamp"), col("close"), col("ema"), col("rsi"), col("signal")
            )
        ).alias("value")
    )

    query = (
        output_stream.writeStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-1.kafka-headless:9092")
        .option("topic", "trading_signals")
        .option("checkpointLocation", "/tmp/spark-checkpoints/signal-generator")
        .start()
    )

    query.awaitTermination()


def main():
    spark = SparkSession.builder.appName("SignalGenerator").getOrCreate()

    process_kafka_messages(spark)


if __name__ == "__main__":
    main()
