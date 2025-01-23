FROM bitnami/spark:latest

WORKDIR /app

USER root
RUN install_packages zip nano
USER 1001

COPY requirements.txt /app/
RUN pip install -r requirements.txt -t dependencies 

WORKDIR /app/dependencies
RUN zip -r ../dependencies.zip .

WORKDIR /app
COPY stream-processor.py /app/
COPY --chmod=555 spark-submit-stream-processor.sh /app/

CMD [ "/app/spark-submit-stream-processor.sh" ]
