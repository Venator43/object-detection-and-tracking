FROM python:3.9.23-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --progress-bar=on -r requirements.txt

COPY . .