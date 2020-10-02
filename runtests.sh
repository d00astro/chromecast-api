#!/bin/bash

docker-compose up -d

docker-compose exec api /bin/sh -c "isort ./**/*.py"
docker-compose exec api black . --exclude env
docker-compose exec api flake8 . --exclude ./env/*
docker-compose exec api python -m pytest --cov="."
docker-compose exec api python -m pytest --cov="."  --cov-report html


