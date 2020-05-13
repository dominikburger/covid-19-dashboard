### Ubuntu base image ###
FROM python:3.8-slim-buster as compile_image

MAINTAINER Dominik Burger <dominik.burger@gmx.org>

RUN apt update && apt install -y --no-install-recommends curl gcc subversion
RUN pip install --user geopandas==0.7

RUN useradd --create-home appuser
RUN mkdir /home/appuser/app
COPY . /home/appuser/app
WORKDIR /home/appuser/app

ENV PYTHONPATH="$PYTHONPATH:."
RUN ["python3", "src/data/download_covid_data.py", "svn"]
RUN ["python3", "src/data/make_dataset.py"]
RUN ["python3", "src/data/download_geo_data.py"]
RUN ["python3", "src/data/make_geo_reference.py"]


FROM python:3.8-slim-buster AS build-image

RUN useradd --create-home appuser
RUN mkdir /home/appuser/app
WORKDIR /home/appuser/app
USER appuser

COPY --from=compile_image /home/appuser/app/ /home/appuser/app/

COPY requirements.txt .
RUN pip install --user -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:."
EXPOSE 8050
ENTRYPOINT ["python3", "src/visualization/layout.py"]