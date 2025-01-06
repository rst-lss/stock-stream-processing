FROM bitnami/spark:latest

ENV SPARK_APPLICATION_PYTHON_LOCATION /app/stream-processor.py

WORKDIR /app

COPY stream-processor.py /app/
COPY --chmod=777 stream-processor-deploy.sh /app/

ENTRYPOINT ["/app/stream-processor-deploy.sh"]
