# =============================================================================
# Sea Cox's Fire & Safety LLC — Production Dockerfile
# =============================================================================
# Minimal, single-stage build using Python 3.12 slim
# No database, no Nginx — just Django + Gunicorn + WhiteNoise
# =============================================================================

FROM python:3.12-slim

# ── Environment variables ────────────────────────────────────────────
# Prevent Python from writing .pyc files and enable unbuffered output
# (unbuffered ensures logs appear immediately in `docker logs`)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ── Set working directory ────────────────────────────────────────────
WORKDIR /app

# ── Install system dependencies ──────────────────────────────────────
# Only what we need: gcc for Pillow, libjpeg/zlib for image support
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libjpeg62-turbo-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Install Python dependencies ──────────────────────────────────────
# Copy requirements first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy project files ───────────────────────────────────────────────
COPY . .

# ── Create logs directory ────────────────────────────────────────────
RUN mkdir -p /app/logs

# ── Collect static files ─────────────────────────────────────────────
# WhiteNoise serves them directly — no Nginx needed
RUN python manage.py collectstatic --noinput

# ── Create non-root user for security ────────────────────────────────
RUN addgroup --system appuser && \
    adduser --system --ingroup appuser appuser && \
    chown -R appuser:appuser /app
USER appuser

# ── Expose port ──────────────────────────────────────────────────────
EXPOSE 8000

# ── Health check ─────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# ── Start Gunicorn ───────────────────────────────────────────────────
# Workers = (2 × CPU cores) + 1 — default 3 is fine for a small site
CMD ["gunicorn", \
     "sea_cox_v2.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
