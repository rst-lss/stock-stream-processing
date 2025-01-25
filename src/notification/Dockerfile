FROM bitnami/spark:latest

WORKDIR /app
COPY notification.py /app/
COPY --chmod=555 spark-submit-notification.sh /app/

CMD [ "/app/spark-submit-notification.sh" ]
