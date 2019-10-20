FROM python:3.7-alpine

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache --virtual .build-deps \
    gcc \
    build-base \
    libffi-dev \
    openssl-dev \
    libxml2-dev \
    libxslt-dev

RUN pip install beautifulsoup4 lxml requests python-dateutil


COPY . /app
WORKDIR /app
CMD python scraping/app.py
