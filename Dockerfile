FROM python:3.8.6-buster

ADD casehub /code
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
