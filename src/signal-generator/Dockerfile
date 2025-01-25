FROM bitnami/spark:latest

WORKDIR /app

COPY signal-generator.py /app/
COPY --chmod=555 spark-submit-signal-generator.sh /app/

CMD [ "/app/spark-submit-signal-generator.sh" ]
