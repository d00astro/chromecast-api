# pull official base image
FROM python:3.8.3-slim-buster

ARG app_name=api

# set working directory
RUN mkdir -p /usr/src
WORKDIR /usr/src

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./requirements-test.txt .
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# add app
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]
