# ============================================================
# STAGE 1: Builder
# Same pattern as the API — install deps here, discard afterwards.
# ============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================================
# STAGE 2: Final
# ============================================================
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password --gecos "" appuser
USER appuser

# The worker has no HTTP port — it doesn't serve web traffic.
# It only talks to Redis. So no EXPOSE needed.

# HEALTHCHECK for the worker is different — there's no HTTP endpoint.
# Instead we check if the Python process is actually running.
# We look for the worker.py process in the process list.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python worker.py" || exit 1

CMD ["python", "worker.py"]