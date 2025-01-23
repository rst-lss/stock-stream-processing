FROM bitnami/spark:latest

USER root
RUN install_packages nano
USER 1001

WORKDIR /app
COPY notification.py /app/
COPY --chmod=555 spark-submit-notification.sh /app/

CMD [ "/app/spark-submit-notification.sh" ]
