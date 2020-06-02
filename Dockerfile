FROM python:3.8.3-alpine3.11
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev build-base
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY casehub .