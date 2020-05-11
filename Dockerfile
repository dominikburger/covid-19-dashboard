### Ubuntu base image ###
FROM python:3.7-slim-buster

MAINTAINER Dominik Burger <dominik.burger@gmx.org>


RUN apt update && apt install -y --no-install-recommends curl gcc git python3.7

RUN mkdir /install
WORKDIR /install
COPY requirements.txt .
RUN pip install --user -r requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

# RUN useradd --create-home appuser
# WORKDIR /home/appuser
# USER appuser

EXPOSE 8050

ENV PYTHONPATH="$PYTHONPATH:."
ENTRYPOINT ["/usr/bin/python3.7", "src/visualization/layout.py"]
