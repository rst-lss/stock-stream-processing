#!/bin/bash
/opt/bitnami/spark/bin/spark-submit \
    --master spark://spark-master-service:7077 \
    --deploy-mode client \
    --name "StreamProcessor" \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 \
    --driver-memory 1g \
    --conf spark.driver.maxResultSize=1g \
    --executor-cores 1 \
    --executor-memory 1g \
    --total-executor-cores 1 \
    --conf spark.executor.instances=1 \
    --conf spark.driver.bindAddress=0.0.0.0 \
    --conf spark.driver.host=stream-processor-service \
    --conf spark.driver.port=7072 \
    --conf spark.driver.blockManager.port=35635 \
    --py-files dependencies.zip \
    /app/stream-processor.py
