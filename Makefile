DOCKER_USER=macadmins
ADMIN_PASS=pass
MACNAMER_PORT=8000
DB_NAME=sal
DB_PASS=password
DB_USER=admin
DB_CONTAINER_NAME:=postgres-sal
NAME:=macnamer
PLUGIN_DIR=/tmp/plugins
# DOCKER_RUN_COMMON=--name="$(NAME)" -p ${MACNAMER_PORT}:8000 --link $(DB_CONTAINER_NAME):db -e ADMIN_PASS=${ADMIN_PASS} -e DB_NAME=$(DB_NAME) -e DB_USER=$(DB_USER) -e DB_PASS=$(DB_PASS) -v ${PLUGIN_DIR}:/home/app/sal/plugins ${DOCKER_USER}/macnamer

DOCKER_RUN_COMMON=--name="$(NAME)" -p ${MACNAMER_PORT}:8000 -e ADMIN_PASS=${ADMIN_PASS} ${DOCKER_USER}/macnamer

all: build

build:
	docker build -t="${DOCKER_USER}/${NAME}" .

build-nocache:
	docker build --no-cache=true -t="${DOCKER_USER}/${NAME}" .

run:
	docker run -d ${DOCKER_RUN_COMMON}

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
	mkdir -p /Users/Shared/postgres
	docker run --name="${DB_CONTAINER_NAME}" -d -v /Users/Shared/postgres:/var/lib/postgresql/data postgres

postgres-clean:
	docker stop $(DB_CONTAINER_NAME)
	docker rm $(DB_CONTAINER_NAME)