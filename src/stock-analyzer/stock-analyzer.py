import redis
from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import *
from pyspark.sql.types import *


# Function to create Spark session
def create_spark_session():
    return SparkSession.builder.appName("StockAnalyzer").getOrCreate()


# Function to calculate technical indicators
def calculate_indicators(df):
    # Define a consistent window size for all indicators
    window_size = 14

    # Moving Average (window size = 14)
    df = df.withColumn(
        "moving_average",
        round(
            avg("close").over(
                Window.orderBy("timestamp").rowsBetween(-(window_size - 1), 0)
            ),
            4,
        ),
    )

    # Exponential Moving Average (window size = 14, smoothing factor = 2 / (N + 1))
    alpha = 2 / (window_size + 1)
    window_spec = Window.orderBy("timestamp")

    df = df.withColumn("prev_ema", lag("close", 1).over(window_spec))
    df = df.withColumn(
        "ema",
        round(
            when(
                col("prev_ema").isNotNull(),
                alpha * col("close") + (1 - alpha) * col("prev_ema"),
            ).otherwise(col("close")),
            4,
        ),
    )

    # Relative Strength Index (RSI, period = 14)
    df = df.withColumn(
        "change", col("close") - lag("close", 1).over(Window.orderBy("timestamp"))
    )
    df = df.withColumn("gain", when(col("change") > 0, col("change")).otherwise(0))
    df = df.withColumn("loss", when(col("change") < 0, -col("change")).otherwise(0))

    gain_avg = avg(col("gain")).over(
        Window.orderBy("timestamp").rowsBetween(-(window_size - 1), 0)
    )
    loss_avg = avg(col("loss")).over(
        Window.orderBy("timestamp").rowsBetween(-(window_size - 1), 0)
    )

    df = df.withColumn("rs", gain_avg / loss_avg)
    df = df.withColumn(
        "rsi",
        round(when(loss_avg == 0, 100).otherwise(100 - (100 / (1 + col("rs")))), 4),
    )

    return df


# Function to push data to Redis
def push_to_redis(json_data):
    try:
        redis_client = redis.StrictRedis(host="redis", port=6379, db=0)
        redis_client.rpush("stock_indicators", json_data)
    except Exception as e:
        print(f"Error pushing to Redis: {str(e)}")


# Batch processing function
def process_batch(df, epoch_id):
    try:
        schema = StructType(
            [
                StructField("timestamp", StringType(), True),
                StructField("open", DoubleType(), True),
                StructField("high", DoubleType(), True),
                StructField("low", DoubleType(), True),
                StructField("close", DoubleType(), True),
                StructField("volume", IntegerType(), True),
            ]
        )

        parsed_df = df.select(
            from_json(col("value").cast("string"), schema).alias("parsed_value")
        ).select("parsed_value.*")

        # Convert timestamp to appropriate format
        parsed_df = parsed_df.withColumn("timestamp", to_timestamp("timestamp"))

        # Calculate technical indicators
        enriched_df = calculate_indicators(parsed_df)

        # Write enriched data back to Kafka
        kafka_output = enriched_df.select(
            to_json(
                struct(
                    "timestamp",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "moving_average",
                    "ema",
                    "rsi",
                )
            ).alias("value")
        )

        kafka_output.write.format("kafka").option(
            "kafka.bootstrap.servers", "kafka-b:9092"
        ).option("topic", "stock_indictors").save()

        # Push data to Redis
        enriched_data = enriched_df.select(
            to_json(
                struct(
                    "timestamp",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "moving_average",
                    "ema",
                    "rsi",
                )
            ).alias("json_value")
        ).collect()

        for row in enriched_data:
            push_to_redis(row.json_value)

        print(f"Batch {epoch_id} processed successfully")

    except Exception as e:
        print(f"Error processing batch {epoch_id}: {str(e)}")


# Main function
def main():
    spark = create_spark_session()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "stock_data")
        .option("startingOffsets", "latest")
        .load()
    )

    query = df.writeStream.foreachBatch(process_batch).outputMode("update").start()

    query.awaitTermination()


if __name__ == "__main__":
    main()
