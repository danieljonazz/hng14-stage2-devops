# ============================================================
# STAGE 1: Builder
# This stage installs dependencies. We use a full image here
# because we need pip and build tools. We'll throw this away
# after — it never goes into production.
# ============================================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy ONLY the requirements file first.
# Why? Docker caches each line. If requirements.txt hasn't changed,
# Docker skips the pip install entirely on future builds — saving minutes.
# If you copied all files first, any code change would bust this cache.
COPY requirements.txt .

# Install packages into a custom prefix folder /install
# Why --no-cache-dir? Removes pip's download cache — we don't need it
# in the image, it just wastes space.
# Why --prefix=/install? So we can copy JUST the installed packages
# into the final stage cleanly, without copying all of Python itself.
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ============================================================
# STAGE 2: Final (Production Image)
# This is what actually runs. It's lean — no pip, no build tools,
# no cache. Just Python + your installed packages + your code.
# ============================================================
FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Copy installed packages from the builder stage.
# /usr/local is where Python looks for packages by default.
COPY --from=builder /install /usr/local

# Copy application source code
COPY . .

# PYTHONUNBUFFERED=1 turns off Python's stdout buffering globally.
# This means print() output appears in docker logs immediately.
# We also added flush=True in the code — belt AND suspenders approach.
ENV PYTHONUNBUFFERED=1

# Create a non-root user called "appuser".
# Why? If someone exploits a vulnerability in your app, they get
# "appuser" access — not root access to the entire container host.
# This is standard production security practice.
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Tell Docker this container listens on port 8000.
# This is documentation — it doesn't actually open the port.
# The actual port binding happens in docker-compose.yml.
EXPOSE 8000

# HEALTHCHECK tells Docker how to test if this service is alive.
# --interval=30s  → check every 30 seconds
# --timeout=10s   → if the check takes more than 10s, it fails
# --start-period=5s → give the app 5s to start before checking
# --retries=3     → fail 3 times in a row before marking as unhealthy
# The actual check: hit the /health endpoint. Exit 0 = healthy, exit 1 = sick.
# Note: you need to add a /health endpoint to main.py (we'll do that next)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# The command that starts the app.
# --host 0.0.0.0 means "accept connections from any IP" — required in Docker.
# Without this, uvicorn would only listen on 127.0.0.1 (itself) and
# no other container could reach it.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]