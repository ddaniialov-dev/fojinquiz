FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./ /code
WORKDIR /code

RUN apk add --no-cache build-base

RUN pip install -r requirements.txt
