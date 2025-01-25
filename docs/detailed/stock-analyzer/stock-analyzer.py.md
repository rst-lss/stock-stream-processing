# `stock-analyzer.py`

## Spark Session Creation

```python
def create_spark_session():
    return SparkSession.builder.appName("StockAnalyzer").getOrCreate()
```
The `create_spark_session` function initializes a Spark session with the application name "StockAnalyzer". This session is essential for running distributed computations on the stock data.


## Technical Indicators Calculation
```python
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
```

The `calculate_indicators` function computes three key technical indicators for stock analysis:

### Moving Average (MA)
A 14-day moving average is calculated using a rolling window. The `avg` function computes the average of the "close" prices over the specified window, and the result is rounded to 4 decimal places.

### Exponential Moving Average (EMA)
The EMA is calculated using a smoothing factor (`alpha = 2 / (window_size + 1)`). The formula `alpha * close + (1 - alpha) * prev_ema` is applied, where `prev_ema` is the previous EMA value. The result is also rounded to 4 decimal places.

### Relative Strength Index (RSI)
RSI is calculated using a 14-day period. The formula involves computing the average gain and loss over the window, calculating the relative strength (`rs = gain_avg / loss_avg`), and then deriving the RSI using `100 - (100 / (1 + rs))`. The result is rounded to 4 decimal places.

## Redis Data Push
The `push_to_redis` function pushes the enriched stock data (in JSON format) to a Redis list named "stock_indicators". This allows for real-time access to the computed indicators.

```python
def push_to_redis(json_data):
    try:
        redis_client = redis.StrictRedis(host="redis", port=6379, db=0)
        redis_client.rpush("stock_indicators", json_data)
    except Exception as e:
        print(f"Error pushing to Redis: {str(e)}")
```

## Batch Processing
```python
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

        parsed_df = parsed_df.withColumn("timestamp", to_timestamp("timestamp"))

        enriched_df = calculate_indicators(parsed_df)

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
            "kafka.bootstrap.servers", "kafka-1.kafka-headless:9092"
        ).option("topic", "stock_indicators").save()

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
```
The `process_batch` function processes incoming stock data in batches. It performs the following steps:
1. Parses the incoming Kafka data into a structured DataFrame.
2. Converts the "timestamp" column to a proper timestamp format.
3. Enriches the data by calculating technical indicators using `calculate_indicators`.
4. Writes the enriched data back to Kafka in JSON format.
5. Pushes the enriched data to Redis for real-time access.

## Main Function
```python
def main():
    spark = create_spark_session()

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "kafka-0.kafka-headless:9092")
        .option("subscribe", "stock_data")
        .option("startingOffsets", "latest")
        .load()
    )

    query = df.writeStream.foreachBatch(process_batch).outputMode("update").start()

    query.awaitTermination()


if __name__ == "__main__":
    main()
```

The `main` function sets up the Spark streaming job:
1. Reads stock data from a Kafka topic named "stock_data".
2. Processes each batch of data using the `process_batch` function.
3. Starts the streaming query and waits for termination.

