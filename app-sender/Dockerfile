FROM python:3 as production_image

ENV SCAN_INTERVAL="10"
ENV INPUT_DIR="/usr/src/app-sender/input"
ENV ENCRYPTION_KEY="/run/secrets/encryption_key"
ENV STATUS_DB_PATH="/usr/src/app-sender/status-db"
ENV RECEIVER_ADDRESS="127.0.0.1"
ENV RECEIVER_PORT="8080"
ENV RECEIVER_URI="/upload"

WORKDIR /usr/src/app-sender

COPY ./sender ./sender/
COPY Pipfile ./
COPY Pipfile.lock ./

RUN mkdir -p /usr/src/app-sender/status-db \
    && mkdir -p /usr/src/app-sender/input
RUN pip install --no-cache-dir pipenv
RUN pipenv install  --system --deploy --ignore-pipfile

ENTRYPOINT ["python", "sender"]