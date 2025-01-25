# `signal-generator.py`

## Signal Generation Logic (`generate_signals`)

```python
def generate_signals(parsed_stream):
    return parsed_stream.withColumn(
        "signal",
        when((col("rsi") < 30) & (col("close") < col("ema")), "buy")
        .when((col("rsi") > 70) & (col("close") > col("ema")), "sell")
        .otherwise("hold"),
    )
```

The function `generate_signals` processes a parsed stream of stock market data and generates trading signals:
- **Buy Signal**: If the RSI is below 30 and the closing price is below the EMA.
- **Sell Signal**: If the RSI is above 70 and the closing price is above the EMA.
- **Hold Signal**: For all other conditions.


## Kafka Message Processing (`process_kafka_messages`)
This function defines the pipeline for consuming data from Kafka, processing it, and producing output back to Kafka.

### Input Schema
The schema for incoming Kafka messages includes fields like `timestamp`, `open`, `close`, `volume`, `ema`, and `rsi`.

```python
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
```

### Reading from Kafka
The script consumes raw data from the `stock_indicators` Kafka topic using Spark's structured streaming.

```python
raw_stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka-1.kafka-headless:9092")
    .option("subscribe", "stock_indicators")
    .option("startingOffsets", "latest")
    .load()
)
```

### Parsing the Stream
```python
parsed_stream = raw_stream.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")
```
The incoming Kafka messages are parsed into structured data based on the defined schema.


### Generating and Publishing Trading Signals
```python
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
```
Trading signals are generated using the `generate_signals` function. The output is formatted as JSON and sent to the `trading_signals` Kafka topic.


## Entry Point

```python
def main():
    spark = SparkSession.builder.appName("SignalGenerator").getOrCreate()
    process_kafka_messages(spark)

if __name__ == "__main__":
    main()
```

The script starts execution with the `main` function.
The script initializes a Spark session and starts the Kafka message processing pipeline.