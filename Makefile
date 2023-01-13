DOCKER_USER=nielshojen
ADMIN_PASS=password
MACNAMER_PORT=8000
DB_NAME=macnamer
DB_PASS=password
DB_USER=macnamer
DB_CONTAINER_NAME:=postgres
DB_CONTAINER_IMAGE:=postgres:12
NAME:=macnamer
TAG:=latest
PLUGIN_DIR=/tmp/plugins

DOCKER_RUN_POSTGRES=--name="$(NAME)" -p ${MACNAMER_PORT}:8000 --link $(DB_CONTAINER_NAME):db -v $(shell pwd)/dockerdata/db:/home/app/macnamer/db -e ADMIN_PASS=${ADMIN_PASS} -e DB_NAME=$(DB_NAME) -e DB_USER=$(DB_USER) -e DB_PASS=$(DB_PASS) ${DOCKER_USER}/${NAME}:${TAG}

DOCKER_RUN=--name="$(NAME)" -p ${MACNAMER_PORT}:8000 -v $(shell pwd)/dockerdata/db:/home/app/macnamer/db -e DEBUG="True" -e ADMIN_PASS=${ADMIN_PASS} ${DOCKER_USER}/${NAME}:${TAG}


all: build

build:
	docker build --tag "${DOCKER_USER}/${NAME}:${TAG}" .

build-nocache:
	docker build --no-cache --tag "${DOCKER_USER}/${NAME}:${TAG}" .

run:
	docker run -d ${DOCKER_RUN}

run-postgres:
	docker run -d ${DOCKER_RUN_POSTGRES}

interactive:
	docker run -i ${DOCKER_RUN_COMMON}

bash:
	docker run -t -i ${DOCKER_RUN_COMMON} /bin/bash

clean:
	docker stop $(NAME)
	docker rm $(NAME)

rmi:
	docker rmi ${DOCKER_USER}/${NAME}

postgres:
	docker pull ${DB_CONTAINER_IMAGE}
	docker run -d --name="${DB_CONTAINER_NAME}" -p 5432:5432 -e POSTGRES_DB=${DB_NAME} -e POSTGRES_USER=${DB_USER} -e POSTGRES_PASSWORD=${DB_PASS} ${DB_CONTAINER_IMAGE}

postgres-clean:
	docker stop $(DB_CONTAINER_NAME)
	docker rm $(DB_CONTAINER_NAME)