#!/bin/bash

echo "
 ██ ▄█▀ █    ██  ▄▄▄▄   ▓█████  ██▀███   ███▄    █ ▓█████▄▄▄█████▓▓█████   ██████ 
 ██▄█▒  ██  ▓██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓█   ▀ ▒██    ▒ 
▓███▄░ ▓██  ▒██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒███   ░ ▓██▄   
▓██ █▄ ▓▓█  ░██░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ▒▓█  ▄   ▒   ██▒
▒██▒ █▄▒▒█████▓ ░▓█  ▀█▓░▒████▒░██▓ ▒██▒▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▒████▒▒██████▒▒
▒ ▒▒ ▓▒░▒▓▒ ▒ ▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░   ░░ ▒░ ░▒ ▒▓▒ ▒ ░
░ ░▒ ▒░░░▒░ ░ ░ ▒░▒   ░  ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░ ░ ░  ░   ░     ░ ░  ░░ ░▒  ░ ░
░ ░░ ░  ░░░ ░ ░  ░    ░    ░     ░░   ░    ░   ░ ░    ░    ░         ░   ░  ░  ░  
░  ░      ░      ░         ░  ░   ░              ░    ░  ░           ░  ░      ░  
                      ░                                                           
"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}\n"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_message "$RED" "Error: $1 is not installed"
        exit 1
    fi
}

check_status() {
    if [ $? -eq 0 ]; then
        print_message "$GREEN" "✓ $1"
    else
        print_message "$RED" "✗ $1"
        exit 1
    fi
}

print_message "$YELLOW" "Checking required tools @_@..."
check_command "minikube"
check_command "kubectl"
check_command "docker"
check_status "You have all the tools we need"

print_message "$YELLOW" "Starting Minikube..."
if ! minikube status | grep -q "Running"; then
    minikube start --feature-gates=PodIndexLabel=true --cpus="4" --memory="9g" 
    check_status "Minikube started"
else
    print_message "$GREEN" "✓ Minikube is already running"
fi

# print_message "$YELLOW" "Enabling Ingress addon..."
# minikube addons enable ingress
# check_status "Ingress addon enabled"

print_message "$YELLOW" "Switching to Minikube's Docker daemon..."
eval $(minikube docker-env)
check_status "Switched to Minikube's Docker daemon"

print_message "$YELLOW" "Building Data Ingestor Docker image..."
docker build -t data-ingestor:latest ./src/data-ingestor/
check_status "Docker images built"

print_message "$YELLOW" "Building Stream Processor Docker image..."
docker build -t stream-processor:latest ./src/stream-processor/
check_status "Docker images built"

print_message "$YELLOW" "Building Notification Docker image..."
docker build -t notification:latest ./src/notification/
check_status "Docker images built"

print_message "$YELLOW" "Building Backend Docker image..."
docker build -t backend:latest ./src/backend/
check_status "Docker images built"

print_message "$YELLOW" "Applying Kubernetes configurations..."
kubectl apply -f src/kafka-cluster/zookeeper-deployment.yaml
sleep 5 
kubectl apply -f src/kafka-cluster/kafka-deployment.yaml
sleep 5 
kubectl apply -f src/spark-cluster/spark-master-deployment.yaml
sleep 5
kubectl apply -f src/spark-cluster/spark-worker-deployment.yaml
sleep 5 
kubeclt apply -f src/redis-database/redis-database-deployment.yaml
sleep 5

kubectl apply -f src/data-ingestor/data-ingestor-deployment.yaml
kubectl apply -f src/stream-processor/stream-processor-deployment.yaml
kubectl apply -f src/notification/notification-deployment.yaml
kubectl apply -f src/backend/backend-deployment.yaml
check_status "Deployment configuration applied"

# kubectl apply -f k8s/ingress.yaml
# check_status "Ingress configuration applied"

# print_message "$YELLOW" "Waiting for pods to be ready..."
# kubectl wait --for=condition=ready pod -l app=node-server --timeout=120s
# check_status "Pods are ready"

# print_message "$YELLOW" "Getting ingress IP..."
# echo "Service URL:"
# minikube ip

echo -e "\nPod Status:"
kubectl get pods

print_message "$GREEN" "Deployment completed successfully!"
print_message "$YELLOW" "To clean up the deployment, run: ./scripts/cleanup.sh"
