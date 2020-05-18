### Ubuntu base image ###
FROM python:3.8-slim-buster

MAINTAINER Dominik Burger <dominik.burger@gmx.org>

RUN apt update && apt install -y --no-install-recommends curl gcc git

RUN useradd --create-home appuser
RUN mkdir /home/appuser/app
COPY . /home/appuser/app
WORKDIR /home/appuser/app
# USER appuser

COPY requirements.txt .
RUN pip install --user -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:."
ENTRYPOINT ["python3", "src/visualization/app.py"]
EXPOSE 8050
