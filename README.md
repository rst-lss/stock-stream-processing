# Stock Stream Processing

A real-time distributed stock data processing system built with modern stream processing technologies.

**Authors:** Amin Haeri & Alireza Nazari

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Usage](#usage)
- [License](#license)

## Overview

Stock Stream Processing is a scalable, distributed system designed to process and analyze real-time stock market data. The system leverages Apache Kafka for stream ingestion, Apache Spark for data processing, and Redis for caching and real-time notifications.

## Architecture

For detailed architecture documentation, refer to:

- **Detailed Documentation**: [Markdown Docs](./docs/detailed/)
- **C4 Model Diagrams**: [Interactive C4 Model](https://s.icepanel.io/LdSOSa16hxVgSR/sGX5)

## Prerequisites

Ensure the following tools are installed on your system:

| Tool            | Purpose                  | Installation Guide                                           |
| --------------- | ------------------------ | ------------------------------------------------------------ |
| **Minikube**    | Local Kubernetes cluster | [Install Minikube](https://minikube.sigs.k8s.io/docs/start/) |
| **Kubectl**     | Kubernetes CLI           | [Install Kubectl](https://kubernetes.io/docs/tasks/tools/)   |
| **Docker**      | Container runtime        | [Install Docker](https://docs.docker.com/get-docker/)        |
| **Python 3.9+** | Test client runtime      | [Install Python](https://www.python.org/downloads/)          |

### Verify Installation

```bash
minikube version
kubectl version --client
docker --version
python --version
```

## Getting Started

### Quick Start Guide

1. **Install Prerequisites** - Ensure all required tools are installed ([see above](#prerequisites))
2. **Optimize Minikube** - Cache Docker images for faster startup ([instructions below](#optimizing-minikube-startup))
3. **Configure API Key** - Set up your Polygon/Massiv API credentials ([see Configuration](#configuration))
4. **Deploy the System** - Run the deployment script ([see Deployment](#deployment))
5. **Connect Test Client** - Use the WebSocket client to view results ([see Usage](#usage))

### Optimizing Minikube Startup

To significantly improve Minikube startup times, pre-cache the required Docker images:

```bash
# Cache all required images
minikube cache add bitnamilegacy/kafka:3.9.0-debian-12-r9
minikube cache add bitnamilegacy/redis:8.0.3-debian-12-r3
minikube cache add bitnamilegacy/spark:3.5.4-debian-12-r5
minikube cache add bitnamilegacy/zookeeper:3.9.3-debian-12-r22
minikube cache add python:3.9-slim
```

Alternatively, cache all images at once:

```bash
# Create a script to cache all images
for image in \
  "bitnamilegacy/kafka:3.9.0-debian-12-r9" \
  "bitnamilegacy/redis:8.0.3-debian-12-r3" \
  "bitnamilegacy/spark:3.5.4-debian-12-r5" \
  "bitnamilegacy/zookeeper:3.9.3-debian-12-r22" \
  "python:3.9-slim"; do
  minikube cache add "$image"
done
```

## Configuration

### API Key Configuration

1. **Obtain API Key**: Sign up at [Polygon/Massiv](https://massive.com/docs/rest/quickstart#authenticate-your-request) to get your API key

2. **Create Environment File**: Copy the example configuration file

   ```bash
   cp .env.example .env
   ```

3. **Add Your Credentials**: Edit `.env` and add your API key

   ```bash
   # Example .env structure
   API_KEY=your_api_key_here
   ```

## Deployment

### Deploy the System

Execute the deployment script to set up the entire stack:

```bash
./scripts/deploy.sh
```

The script will:

1. Start Minikube (if not already running)
2. Deploy Zookeeper and Kafka
3. Deploy Redis
4. Deploy Apache Spark
5. Deploy application services
6. Configure networking and services

### Verify Deployment

Check that all pods are running:

```bash
kubectl get pods
```

Expected output should show all pods in `Running` state.

### Clean Up Resources

To remove all deployed resources:

```bash
./scripts/clean.sh
```

This will delete all Kubernetes resources and optionally stop Minikube.

## Usage

### Access the System

The system currently provides backend services accessible via WebSocket. A graphical interface is planned for future releases.

### Using the Test Client (Python)

1. **Create Virtual Environment**:

   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate it
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install Dependencies**:

   ```bash
   pip install websockets
   ```

3. **Run the Client**:

   ```bash
   python ./src/test-client/client.py
   ```

### Using wscat (Node.js Alternative)

If you have Node.js installed, you can use `wscat` for WebSocket testing:

1. **Install wscat**:

   ```bash
   npm install -g wscat
   ```

2. **Connect to the WebSocket Service**:

   ```bash
   # Get the service URL
   minikube service notification-service --url

   # Connect using wscat
   wscat -c ws://<service-url>
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
