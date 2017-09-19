#!/bin/bash

ARCH="amd64"
REGISTRY="172.24.1.72:6000"

IMAGE="${ARCH}-qrlabs"
DOCKERFILE="${ARCH}.dockerfile"


echo "Building ${IMAGE} from ${DOCKERFILE} ..."
docker build -t ${IMAGE} -f ${DOCKERFILE} .
