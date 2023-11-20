#!/bin/bash

: ${APP_PORT:=8000}
: ${DATABASE_URL:="kitanoyoru:1234@mongodb:16000"}
: ${DATABASE_NAME:="lead_hit_python_task"}
: ${MONGO_PORT:=16000}
: ${MONGO_USERNAME:="kitanoyoru"}
: ${MONGO_PASSWORD:="1234"}

export APP_PORT
export DATABASE_URL
export DATABASE_NAME
export MONGO_PORT
export MONGO_USERNAME
export MONGO_PASSWORD

docker-compose -f docker/docker-compose.yaml up -d
