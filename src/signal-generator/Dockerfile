FROM bitnamilegacy/spark:3.5.4-debian-12-r5

WORKDIR /app

COPY signal-generator.py /app/
COPY --chmod=555 spark-submit-signal-generator.sh /app/

CMD [ "/app/spark-submit-signal-generator.sh" ]
