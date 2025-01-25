# `stock-analyzer-deployment.yaml`

## Deployment Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: stock-analyzer
  labels:
    app: stock-analyzer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: stock-analyzer
  template:
    metadata:
      labels:
        app: stock-analyzer
    spec:
      containers:
        - name: stock-analyzer
          image: stock-analyzer:latest
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 7072
              name: headless-svc
            - containerPort: 8082
              name: web-ui
            - containerPort: 35635
              name: block-manager
          env:
            - name: SPARK_MASTER_URL
              value: spark://spark-master-service:7077
```
- **Replicas**: The application is configured to run with 1 replica.
- **Labels**: The deployment is labeled with `app: stock-analyzer` for easy identification.
- **Container Configuration**:
  - **Image**: The container uses the `stock-analyzer:latest` image.
  - **Ports**: Three ports are exposed:
    - `7072` for headless service.
    - `8082` for the web UI.
    - `35635` for the block manager.
  - **Environment Variables**: The `SPARK_MASTER_URL` environment variable is set to `spark://spark-master-service:7077`, which specifies the Spark master URL for the driver to access master.

## Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: stock-analyzer-service
  labels:
    app: stock-analyzer
spec:
  selector:
    app: stock-analyzer
  ports:
    - port: 7072
      name: headless-svc
    - port: 8082
      name: web-ui
    - port: 35635
      name: block-manager
```
- **Selector**: The service targets pods labeled with `app: stock-analyzer`.
- **Ports**: The same ports as in the deployment are exposed:
  - `7072` for headless service.
  - `8082` for the web UI.
  - `35635` for the block manager.
