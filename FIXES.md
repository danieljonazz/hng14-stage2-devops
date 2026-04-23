# FIXES.md

## Bug 1
- **File:** `api/main.py`
- **Line:** 8
- **Problem:** Redis connection hardcoded to `localhost`. In Docker, `localhost` 
  resolves to the container itself, not the Redis service. Also missing password auth.
- **Fix:** Changed to use environment variables:
  `r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", 6379)), password=os.getenv("REDIS_PASSWORD"))`

## Bug 2
- **File:** `worker/worker.py`
- **Line:** 6
- **Problem:** Same localhost hardcoding as Bug 1 — worker cannot reach Redis container.
- **Fix:** Same env-var-based fix as Bug 1.

## Bug 3
- **File:** `frontend/app.js`
- **Line:** 6
- **Problem:** API URL hardcoded to `http://localhost:8000`. Frontend container 
  cannot reach the API container via localhost.
- **Fix:** `const API_URL = process.env.API_URL || "http://api:8000";`

## Bug 4
- **File:** `worker/worker.py`
- **Line:** 9
- **Problem:** `print()` without `flush=True`. Python buffers stdout by default, 
  causing logs to be delayed or invisible in `docker logs`.
- **Fix:** `print(f"Processing job {job_id}", flush=True)`

## Bug 5
- **File:** `worker/worker.py`
- **Line:** 12
- **Problem:** Same stdout buffering issue as Bug 4.
- **Fix:** `print(f"Done: {job_id}", flush=True)`

## Bug 6
- **File:** `worker/worker.py`
- **Line:** 14
- **Problem:** `while True` loop with no SIGTERM handler. Docker sends SIGTERM 
  on container stop — unhandled, it force-kills the worker after timeout, 
  dropping any in-progress jobs.
- **Fix:** Added signal handler with a `run` flag to exit the loop gracefully.
## Bug 9
- **File:** `api/main.py`
- **Line:** N/A (missing)
- **Problem:** No /health endpoint exists. The Docker HEALTHCHECK 
  and docker-compose dependency checks require this to confirm the 
  API is ready — without it, the container is always marked unhealthy.
- **Fix:** Added GET /health route returning {"status": "ok"}

## Bug 10
- **File:** `api/.env`
- **Line:** N/A
- **Problem:** .env file sitting inside api/ folder gets copied into 
  the Docker image via `COPY . .`, exposing the Redis password 
  inside the built image.
- **Fix:** Added api/.dockerignore to exclude .env from the image. 
  Moved required variables to root .env for docker-compose to consume.