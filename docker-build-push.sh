#!/bin/bash

source .env
echo $DOCKER_PASSWORD docker login -u $DOCKER_USERNAME --password-stdin &>/dev/null
docker build . --push -t $DOCKER_USERNAME/rtu_mirea_vuc_schedule:latest
