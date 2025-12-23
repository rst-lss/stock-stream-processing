# `backend-deployment.yaml`

This file defines the deployment configuration for the `backend` service using Kubernetes. It specifies the deployment's metadata, desired state, and environment variable configuration.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
```
This specifies the type of Kubernetes object (`Deployment`). The `metadata` section assigns the name `backend` to this deployment for identification.

```yaml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: backend
```
- `replicas: 1` ensures one replica (pod) of the `backend` application is running.
- `selector.matchLabels` identifies pods that match the `app: backend` label for this deployment.

```yaml
  template:
    metadata:
      labels:
        app: backend
```
The `template` specifies the configuration of pods managed by the deployment. The `metadata.labels` section assigns the label `app: backend` to the pod, aligning with the selector.

```yaml
    spec:
      containers:
        - name: backend
          image: backend:latest
          imagePullPolicy: Never
```

The `imagePullPolicy` ensures the image is pulled locally from minikube cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
```
This specifies the API version (`v1`) and type (`Service`). The `metadata` assigns the name `backend-service` to this service.

```yaml
spec:
  selector:
    app: backend
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
```
- `selector.app: backend` ties the service to pods labeled `app: backend`.
- `ports` defines the network configuration:
- `protocol: TCP` specifies TCP as the communication protocol.
- `port: 5000` exposes the service on port 5000.
- `targetPort: 5000` maps the service to port 5000 on the pods.

