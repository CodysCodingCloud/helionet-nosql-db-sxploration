#!/usr/bin/env bash
# bash t_mongo.sh 0 dev 5
STEP=${1:-"1"}
if [ "$STEP" = "0" ]; then
# docker run -d --name some-mongo -p 27017:27017 -v mongo-data:/data/db -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=pass12345 mongo:latest
    sudo docker-compose up --build
elif [ "$STEP" = "1" ]; then
    docker-compose up
elif [ "$STEP" = "666" ]; then
    docker compose down -v
fi