#!/bin/bash
/opt/spark/bin/spark-submit \
  --master ${SPARK_MASTER_URL} \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 \
  ${SPARK_APPLICATION_PYTHON_LOCATION}
