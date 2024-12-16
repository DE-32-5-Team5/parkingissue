FROM mysql:latest

COPY ./config/default.conf /etc/mysql/conf.d/
COPY ./init/initialize.sql /docker-entrypoint-initdb.d/init.sql
COPY ./init/parkingarea_information.csv /var/lib/mysql-files/
COPY ./init/parkingarea_operationtime.csv /var/lib/mysql-files/
COPY ./init/parkingarea_operationcharge.csv /var/lib/mysql-files/
COPY ./init/parkingarea_realtime.csv /var/lib/mysql-files/

ARG MYSQL_ROOT_PASSWORD
ARG MYSQL_DATABASE
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
