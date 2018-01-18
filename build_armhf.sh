#!/bin/bash

ARCH="armhf"

IMAGE="${ARCH}-qrlabs"
DOCKERFILE="${ARCH}.dockerfile"

echo "Building ${IMAGE} from ${DOCKERFILE} ..."
docker build --build-arg http_proxy="http://www-cache-nrs.si.fr.intraorange:3128/" --build-arg https_proxy="http://www-cache-nrs.si.fr.intraorange:3128/" -t ${IMAGE} -f ${DOCKERFILE} .
#docker build -t ${IMAGE} -f ${DOCKERFILE} .

docker rm -f qrLabs
docker run -d --restart always --name qrLabs -p 80:80 ${IMAGE} 
docker logs -f qrLabs

