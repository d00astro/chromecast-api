# pull official base image
FROM postgres:12-alpine

ARG db_base_name=db

# create database creation scrit to be run on init
RUN echo "CREATE DATABASE ${db_base_name};" > /docker-entrypoint-initdb.d/create.sql \
 && echo "CREATE DATABASE ${db_base_name}_dev;" >> /docker-entrypoint-initdb.d/create.sql \
 && echo "CREATE DATABASE ${db_base_name}_tst;" >> /docker-entrypoint-initdb.d/create.sql

# run init.sql on init
ADD init.sql /docker-entrypoint-initdb.d



