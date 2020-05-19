### Ubuntu base image ###
FROM python:3.8-slim-buster

MAINTAINER Dominik Burger <dominik.burger@gmx.org>

ENV workdir /home/appuser/app

RUN apt update && apt install -y --no-install-recommends curl gcc git

RUN useradd --create-home appuser
USER appuser
RUN mkdir ${workdir}
COPY --chown=appuser . ${workdir}
WORKDIR ${workdir}
RUN pip install --user -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:."
ENTRYPOINT ["python3", "src/app.py"]
WORKDIR /
ENTRYPOINT ["bin/bash"]
EXPOSE 8050
