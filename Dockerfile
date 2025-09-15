FROM python:3.9.23-slim

WORKDIR /app

COPY requirements_docker.txt .

RUN pip install --progress-bar=on -r requirements_docker.txt

COPY . .