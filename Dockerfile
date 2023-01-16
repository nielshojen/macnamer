# Macnamer Dockerfile
#FROM phusion/passenger-customizable:latest
FROM python:3.11.1-alpine3.17

ARG BUILDPLATFORM linux/amd64,linux/arm64

ENV APP_DIR /home/app/macnamer
ENV TZ Europe/Copenhagen
ENV MACNAMER_TZ Europe/Copenhagen
ENV MACNAMER_ADMINS Docker User, docker@localhost
ENV MACNAMER_LANG en_US

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
    gcc \
    build-base \
    linux-headers \
    sqlite \
    postgresql-dev \
    postgresql-libs \
    libpq \
    nginx

#RUN git clone --branch dev https://github.com/nielshojen/macnamer.git $APP_DIR
ADD ./ $APP_DIR
RUN pip3 install -r $APP_DIR/setup/requirements.txt
RUN pip3 install gunicorn
ADD docker/nginx/macnamer.conf /etc/nginx/http.d/macnamer.conf
ADD docker/nginx/nginx.conf /etc/nginx/nginx.conf
ADD docker/settings.py $APP_DIR/macnamer/
RUN mkdir -p $APP_DIR/macnamer/db
ADD docker/settings_import.py $APP_DIR/macnamer/
ADD docker/django/management/ $APP_DIR/namer/management/
ADD docker/gunicorn_config.py $APP_DIR/
ADD docker/run.sh /run.sh
RUN chmod +x /run.sh

EXPOSE 8000

VOLUME ["/home/app/macnamer/db"]

CMD ["/run.sh"]
