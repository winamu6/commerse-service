FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && pip install --upgrade pip setuptools wheel

COPY feedback_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

RUN groupadd -r app && useradd -r -g app app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

COPY feedback_service/src ./src
COPY feedback_service/alembic ./alembic
COPY feedback_service/alembic.ini ./alembic.ini
COPY feedback_service/src/.env ./src/.env

RUN chown -R app:app /app
USER app

EXPOSE 8005

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -qO- --timeout=2 http://127.0.0.1:8005/health || exit 1

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "1"]

