FROM python:3.8.0-slim

WORKDIR /app/scopic_task

COPY ./requirements.txt ./requirements.txt
COPY ./db.sqlite3 ./db.sqlite3

RUN set -xe \
    && apt-get -qqy update \
    && pip --no-cache-dir install --upgrade pip \
    && pip --no-cache-dir install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

COPY ./ ./

ENV PYTHONUNBUFFERED=1 \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8