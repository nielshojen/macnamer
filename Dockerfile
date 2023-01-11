# Macnamer Dockerfile
FROM phusion/passenger-customizable:latest

ARG BUILDPLATFORM linux/amd64,linux/arm64

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
ENV APP_DIR /home/app/macnamer
ENV TZ Europe/Copenhagen
ENV DOCKER_MACNAMER_TZ Europe/Copenhagen
ENV DOCKER_MACNAMER_ADMINS Docker User, docker@localhost
ENV DOCKER_MACNAMER_LANG en_US

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]
RUN apt-get update
RUN apt-get upgrade -y
RUN /pd_build/utilities.sh
RUN /pd_build/python.sh

RUN apt-get -y install \
    build-essential \
    python-setuptools \
    libpq-dev \
    python3-dev \
    python3-pip \
    postgresql-client

#RUN git clone --branch dev https://github.com/nielshojen/macnamer.git $APP_DIR
ADD ./ $APP_DIR
RUN pip3 install -r $APP_DIR/setup/requirements.txt
RUN mkdir -p /etc/my_init.d
ADD docker/nginx/nginx-env.conf /etc/nginx/main.d/
ADD docker/nginx/macnamer.conf /etc/nginx/sites-enabled/macnamer.conf
ADD docker/settings.py $APP_DIR/macnamer/
RUN mkdir -p $APP_DIR/macnamer/db
ADD docker/settings_import.py $APP_DIR/macnamer/
ADD docker/passenger_wsgi.py $APP_DIR/
ADD docker/django/management/ $APP_DIR/namer/management/
ADD docker/run.sh /etc/my_init.d/run.sh
RUN rm -f /etc/service/nginx/down
RUN rm -f /etc/nginx/sites-enabled/default

EXPOSE 8000

VOLUME ["/home/app/macnamer/db"]

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
