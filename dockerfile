FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install .

ENTRYPOINT ["celery", "-A", "wled_state_discovery.wled", "worker"]