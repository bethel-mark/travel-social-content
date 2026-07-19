# travel-social-content API service
FROM python:3.11-slim

LABEL maintainer="travel-social-content contributors"
LABEL description="REST API for travel social-media content generation skill"

WORKDIR /app

# System deps for curl-based search helper
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python deps first (cache layer)
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# Source
COPY SKILL.md ./
COPY references/ ./references/
COPY scripts/ ./scripts/
COPY examples/ ./examples/

# Cache for offline search
RUN mkdir -p /app/cache

# Environment defaults
ENV API_HOST=0.0.0.0 \
    API_PORT=8000 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:${API_PORT}/health || exit 1

CMD ["python", "scripts/api/server.py"]
