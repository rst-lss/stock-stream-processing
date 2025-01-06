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
    minikube start
    check_status "Minikube started"
else
    print_message "$GREEN" "✓ Minikube is already running"
fi

# print_message "$YELLOW" "Enabling Ingress addon..."
# minikube addons enable ingress
# check_status "Ingress addon enabled"

# print_message "$YELLOW" "Switching to Minikube's Docker daemon..."
# eval $(minikube docker-env)
# check_status "Switched to Minikube's Docker daemon"

# print_message "$YELLOW" "Building Consumer Docker image..."
# docker build -t spark-consumer:latest ./src/consumer/
# check_status "Docker images built"

# print_message "$YELLOW" "Building Producer Docker image..."
# docker build -t kafka-producer:latest ./src/producer/
# check_status "Docker images built"

print_message "$YELLOW" "Applying Kubernetes configurations..."
kubectl apply -f src/kafka-cluster/zookeeper-deployment.yaml
kubectl apply -f src/kafka-cluster/kafka-deployment.yaml
# kubectl apply -f src/kafka-cluster/kafka-deployment-b.yaml
# kubectl apply -f src/spark-cluster/spark-services.yaml
# kubectl apply -f src/spark-cluster/spark-master-deployment.yaml
# kubectl rollout status src/spark-cluster/spark-master-deployment.yaml
# kubectl apply -f src/spark-cluster/spark-worker-deployment.yaml
check_status "Deployment configuration applied"

# kubectl apply -f k8s/ingress.yaml
# check_status "Ingress configuration applied"

# print_message "$YELLOW" "Waiting for pods to be ready..."
# kubectl wait --for=condition=ready pod -l app=node-server --timeout=120s
# check_status "Pods are ready"

print_message "$YELLOW" "Getting ingress IP..."
echo "Service URL:"
minikube ip

echo -e "\nPod Status:"
# kubectl get pods -l app=node-server
kubectl get pods

print_message "$GREEN" "Deployment completed successfully!"
print_message "$YELLOW" "To clean up the deployment, run: ./scripts/cleanup.sh"
