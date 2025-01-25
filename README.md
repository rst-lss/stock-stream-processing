# Stock Stream Processing

This repository contains the **Stock Stream Processing** project by **Amin Haeri** and **Alireza Nazari**. The project is designed to handle real-time stock data processing using distributed systems techniques.

## Project Overview

The project implements a stream processing system for analyzing stock data. It leverages modern distributed systems tools and methodologies to achieve scalability and performance.

- **C4 Model Documentation**: [C4 Model Link](https://s.icepanel.io/qIhYcBpM0jN50I/DX37)
- **Video Footage**: [Video Link](https://drive.google.com/file/d/1w2S0W5Zxqcf71tBmCjnsGT-oCJRSxTVE/view?usp=sharing)

## Prerequisites

Before running the project, ensure the following tools are installed:

- **Minikube**
- **Kubectl**
- **Docker**

## Setup and Deployment

### API Key Configuration
To use the system, you need to obtain an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key). Once you have the API key, place it in a `.env` file following the structure provided in `.env.example`.

### Deploying the Project
To deploy the project, run the script located at:
```
/scripts/deploy.md
```

### Cleaning Up
To clean up the deployment, use the following script:
```
/scripts/clean.md
```

### Optimizing Minikube Startup
To speed up the Minikube startup process, cache the following Docker images:

- `bitnami/kafka`
- `bitnami/redis:latest`
- `bitnami/spark:latest`
- `bitnami/zookeeper`
- `python:3.9-slim`

Use the command below to add images to the Minikube cache:
```
minikube cache add <image>
```

## Getting Started

1. Install all prerequisites listed above.
2. Optimize Minikube with the caching instructions.
3. Obtain your API key from Alpha Vantage and configure the `.env` file.
4. Deploy the project using the provided deployment script.
5. Access the system and analyze the results.

