FROM python:3.11

RUN mkdir /src
RUN mkdir /data

WORKDIR /src

RUN apt-get -y update

RUN apt-get -y install libgdal-dev gdal-bin

ENV PYTHONUNBUFFERED 1

COPY main.py /src

ENTRYPOINT python main.py
