FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingestion ./ingestion
COPY events ./events
COPY transformations ./transformations
COPY warehouse ./warehouse
COPY data_quality ./data_quality
COPY scripts ./scripts

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "ingestion.consumer"]
