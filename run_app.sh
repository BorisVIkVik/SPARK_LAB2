#!/bin/bash

docker compose -f ./hadoop/docker-compose.yaml --project-directory ./hadoop up -d
sleep 15 && python src/load.py && python src/main.py