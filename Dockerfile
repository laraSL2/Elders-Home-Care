FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        git \
        wget \
        curl \
        iputils-ping \
        net-tools \
        nano && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p /app/uploads && chmod 777 /app/uploads

ARG GOOGLE_API_KEY
ARG QDRANT_URL
ARG QDRANT_API_KEY
ARG NEO4J_URI
ARG NEO4J_USERNAME
ARG NEO4J_PASSWORD
ARG FLASK_CONFIG
ARG UPLOAD_FOLDER

ENV GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    QDRANT_URL=${QDRANT_URL} \
    QDRANT_API_KEY=${QDRANT_API_KEY} \
    NEO4J_URI=${NEO4J_URI} \
    NEO4J_USERNAME=${NEO4J_USERNAME} \
    NEO4J_PASSWORD=${NEO4J_PASSWORD} \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_CONFIG=${FLASK_CONFIG} \
    UPLOAD_FOLDER=${UPLOAD_FOLDER}

EXPOSE 8001

CMD ["python", "-u", "run.py"]