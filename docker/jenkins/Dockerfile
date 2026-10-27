
FROM jenkins/jenkins:lts-jdk21

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 \
       python3-venv \
       python3-pip \
       unixodbc \
       unixodbc-dev \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
