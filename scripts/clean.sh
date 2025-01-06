#!/bin/bash
echo "Cleaning up deployment..."

kubectl delete -k src/kafka-cluster/zookeeper-deployment.yaml
kubectl delete -k src/kafka-cluster/kafka-deployment.yaml

read -p "Do you want to STOP Minikube container? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    minikube stop
fi

read -p "Do you want to also **DELETE** Minikube container? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    minikube stop
fi

echo "Cleanup completed!"
