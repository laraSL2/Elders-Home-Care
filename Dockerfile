FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /App

COPY . .

ARG GOOGLE_API_KEY
ARG QDRANT_URL
ARG QDRANT_API_KEY
ARG NEO4J_URI
ARG NEO4J_USERNAME
ARG NEO4J_PASSWORD


# ARG GOOGLE_API_KEY="AIzaSyAZKyrdvM6i_RqNtw6snInBGxAhQJ_YxmY"
# ARG QDRANT_URL="https://77760314-7d45-4ffe-8457-e089972349fc.us-east4-0.gcp.cloud.qdrant.io:6333"
# ARG QDRANT_API_KEY="Q_Sr0iqG02_sESUZoKoskwhLBB8HrlGskGeaxNxU1FUtNECxS2IRDg"
# ARG NEO4J_URI="neo4j+s://cccb3852.databases.neo4j.io"
# ARG NEO4J_USERNAME="neo4j"
# ARG NEO4J_PASSWORD="a8dRqfcV-89E4DYks5qM7K9R8RXVBV3I59o1a2i31u0"

ENV GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    QDRANT_URL=${QDRANT_URL} \
    QDRANT_API_KEY=${QDRANT_API_KEY} \
    NEO4J_URI=${NEO4J_URI} \
    NEO4J_USERNAME=${NEO4J_USERNAME} \
    NEO4J_PASSWORD=${NEO4J_PASSWORD}

RUN apt-get update && \
    apt-get install -y python3 python3-pip git wget curl iputils-ping net-tools nano && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["/bin/bash", "-c", "python -u api.py || tail -f /dev/null"]

