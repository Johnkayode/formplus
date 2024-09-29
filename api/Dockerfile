FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /api

WORKDIR /api

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt
