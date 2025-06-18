# ------------------------------------------------------------------------------
# Base image
# ------------------------------------------------------------------------------
FROM python:3.9-slim

COPY requirements.txt ./
RUN apt-get update > /dev/null && apt-get install -y build-essential && pip install --disable-pip-version-check -r requirements.txt

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && echo Asia/Seoul > /etc/timezone
