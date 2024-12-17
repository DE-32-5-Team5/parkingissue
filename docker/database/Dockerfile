FROM mysql:latest

COPY ./config/default.conf /etc/mysql/conf.d/
COPY ./init/initialize.sql /docker-entrypoint-initdb.d/

ARG MYSQL_ROOT_PASSWORD
ARG MYSQL_DATABASE

ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
