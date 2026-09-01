# ── Stage 1: dependency builder ───────────────────────────────────────────
# Using a build stage keeps the final image lean — only compiled wheels
# (not gcc / build tools) end up in the runtime image.
FROM python:3.11-slim AS builder

WORKDIR /build

# Install only the build deps needed for psycopg2 (already using the -binary
# wheel so no libpq-dev needed, but keep the pattern for real psycopg2 swaps).
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime image ────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

LABEL maintainer="Samrudh S Shetty <samrudh9@github>"
LABEL description="Workshop 1 — scrapethissite.com scraper"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source and SQL schema
COPY src/   ./src/
COPY sql/   ./sql/

# Log directory (also mounted as a volume in compose)
RUN mkdir -p /app/logs

# Non-root user for security best-practice
RUN useradd --create-home --shell /bin/bash scraper
USER scraper

# PYTHONPATH so `from models import …` works without a package __init__
ENV PYTHONPATH=/app/src

CMD ["python", "src/main.py"]
