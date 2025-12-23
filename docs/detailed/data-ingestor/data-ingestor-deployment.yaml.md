# `data-ingestor-deployment.yaml`

This file defines the deployment configuration for the `data-ingestor` service using Kubernetes. It specifies the deployment's metadata, desired state, and environment variable configuration.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-ingestor
```
The `kind` indicates the resource type as a `Deployment`. The `metadata` includes the name `data-ingestor` for identification.

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: data-ingestor
```
The `spec` defines the desired state for the deployment. It specifies a single replica for the deployment, meaning only one pod will run. The `selector` ensures the deployment manages pods labeled with `app: data-ingestor`.

```yaml
  template:
    metadata:
      labels:
        app: data-ingestor
```
The `template` section describes the pod configuration. The `metadata` defines labels, which are essential for identifying and managing the pod.

```yaml
    spec:
      containers:
        - name: data-ingestor
          image: data-ingestor:latest
          imagePullPolicy: IfNotPresent
```
The `spec` inside `template` defines the container configuration. The container is named `data-ingestor` and uses the `data-ingestor:latest` image that we added through deploy script. The `imagePullPolicy` ensures the image is pulled locally from minikube cluster.

```yaml
          env:
            - name: KAFKA_BOOTSTRAP_SERVERS
              value: kafka-0.kafka-headless:9092
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: data-ingestor-secret
                  key: API_KEY
            - name: STOCK_SYMBOL
              value: AAPL
            - name: DATA_INTERVAL
              value: 60min
            - name: KAFKA_BROKER
              value: kafka-0.kafka-headless:9092
            - name: KAFKA_TOPIC
              value: stock_data
            - name: FETCH_INTERVAL
              value: '30'
```
The `env` section defines environment variables passed to the container. These variables include:

- `KAFKA_BOOTSTRAP_SERVERS`: Specifies the Kafka broker connection string.
- `API_KEY`: Retrieves the API key from the `data-ingestor-secret` Kubernetes secret that is going to be used in the endpoint.
- `STOCK_SYMBOL`: Defines the stock symbol (e.g., `AAPL`).
- `DATA_INTERVAL`: Sets the interval between the data points that are fetched from the endpoint.
- `KAFKA_BROKER` and `KAFKA_TOPIC`: Configure the Kafka connection and topic.
- `FETCH_INTERVAL`: Determines the frequency of data fetching in seconds.

