FROM python:3.9.23-slim

WORKDIR /app

COPY requirements_docker.txt .

RUN pip install --progress-bar=on -r requirements_docker.txt

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgthread-2.0-0 \
    libfontconfig1 \
    libice6 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxft2 \
    libxi6 \
    libxinerama1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    libxxf86vm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip uninstall -y opencv-python-headless

RUN pip install --no-cache-dir opencv-python-headless
    
COPY . .