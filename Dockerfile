# FROM ubuntu:22.04

# ENV DEBIAN_FRONTEND=noninteractive

# WORKDIR /App

# COPY . .

# ARG GOOGLE_API_KEY
# ARG QDRANT_URL
# ARG QDRANT_API_KEY
# ARG NEO4J_URI
# ARG NEO4J_USERNAME
# ARG NEO4J_PASSWORD


# ENV GOOGLE_API_KEY=${GOOGLE_API_KEY} \
#     QDRANT_URL=${QDRANT_URL} \
#     QDRANT_API_KEY=${QDRANT_API_KEY} \
#     NEO4J_URI=${NEO4J_URI} \
#     NEO4J_USERNAME=${NEO4J_USERNAME} \
#     NEO4J_PASSWORD=${NEO4J_PASSWORD}

# RUN apt-get update && \
#     apt-get install -y python3 python3-pip git wget curl iputils-ping net-tools nano && \
#     update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*


# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8001

# CMD ["/bin/bash", "-c", "python -u api.py || tail -f /dev/null"]

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

ARG GOOGLE_API_KEY
ARG QDRANT_URL
ARG QDRANT_API_KEY
ARG NEO4J_URI
ARG NEO4J_USERNAME
ARG NEO4J_PASSWORD

ENV GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    QDRANT_URL=${QDRANT_URL} \
    QDRANT_API_KEY=${QDRANT_API_KEY} \
    NEO4J_URI=${NEO4J_URI} \
    NEO4J_USERNAME=${NEO4J_USERNAME} \
    NEO4J_PASSWORD=${NEO4J_PASSWORD}

EXPOSE 8001

CMD ["python", "-u", "api.py"]

