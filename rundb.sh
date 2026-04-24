#!/usr/bin/env bash
# bash t_mongo.sh 0 dev 5
STEP=${1:-"1"}
PYARG=${2:-"1"}
DISEASE_ID=${3:-"DOID:0050742"}


if [ "$STEP" = "0" ]; then
# docker run -d --name some-mongo -p 27017:27017 -v mongo-data:/data/db -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=pass12345 mongo:latest
    sudo docker-compose up --build
elif [ "$STEP" = "1" ]; then
    docker-compose up
elif [ "$STEP" = "2" ]; then
    python -m venv .venv
elif [ "$STEP" = "3" ]; then
    source .venv/bin/activate
    python -m pip install -r requirements.txt
elif [ "$STEP" = "4" ]; then
    # for running GUI version of the project 
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python main.py
elif [ "$STEP" = "5" ]; then
    # for running python terminal version of the project 
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    python pyt.py
elif [ "$STEP" = "21" ]; then
    # for running pyspark aggregator with mapreduce
    source .venv/bin/activate
    # java bug
    export JDK_JAVA_OPTIONS="-Djava.security.manager=allow"
    python -m pip install -r requirements.txt
    python pytmr.py
elif [ "$STEP" = "666" ]; then
    docker compose down -v
fi


# Test scripts
case "$STEP" in
    "t1")
    source .venv/bin/activate
    python src/parse_data.py
    ;;
    "t2")
    source .venv/bin/activate
    python test_funcs.py "$PYARG" "$DISEASE_ID"
    ;;
esac