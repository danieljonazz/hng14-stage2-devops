# ============================================================
# STAGE 1: Builder
# Install Node dependencies here. node_modules can be enormous
# (hundreds of MB). Multi-stage lets us only keep what's needed.
# ============================================================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first — same cache optimization logic as Python.
# npm ci is like npm install but:
# - Faster (uses lockfile exactly)
# - Safer (fails if package-lock.json is out of sync)
# - Better for CI/CD environments
COPY package*.json .

RUN npm ci --only=production


# ============================================================
# STAGE 2: Final
# Alpine = a tiny Linux distro (~5MB base). Perfect for production.
# ============================================================
FROM node:18-alpine

WORKDIR /app

# Copy installed node_modules from builder
COPY --from=builder /app/node_modules ./node_modules

# Copy the rest of the app
COPY . .

# Create and switch to non-root user
# Alpine uses a different syntax than Debian for creating users
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 3000

# HEALTHCHECK hits the root of the frontend server.
# If Express is up and serving, this returns 200 = healthy.
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:3000 || exit 1

CMD ["node", "app.js"]