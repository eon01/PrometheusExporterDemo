# syntax=docker/dockerfile:1

FROM python:3.12-slim

# Prevents Python from writing .pyc files and enables unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 10001 appuser

# Install runtime deps (curl only for HEALTHCHECK; drop if you don’t want it)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Drop privileges
USER appuser

EXPOSE 8000

# Optional: basic healthcheck (checks the /metrics endpoint)
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3  CMD curl -fsS http://localhost:8000/metrics >/dev/null || exit 1

CMD ["python", "app.py"]

