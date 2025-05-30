# Makefile
# Variables
PROJECT_NAME=robin
SERVICE=product_api

# ---------------------------
# 🐳 Docker
# ---------------------------

up:
	docker-compose up

build:
	docker-compose build

start: build up

down:
	docker-compose down

restart: down up

# ---------------------------
# 🧰 Dev utils
# ---------------------------

shell:
	docker exec -it $$(docker ps -qf "name=${SERVICE}") /bin/bash

logs:
	docker-compose logs -f ${SERVICE}

py:
	docker exec -it $$(docker ps -qf "name=${SERVICE}") poetry run python

seed:
	docker exec -it $(docker ps -qf "name=product_api") poetry run python seed.py
