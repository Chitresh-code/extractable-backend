FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps (keep minimal; add others if your PDF stack needs them)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (lockfile-aware, fast)
RUN pip install --no-cache-dir uv

# Workdir inside the image
WORKDIR /app

# Copy lockfiles first (from repo root) for better caching
# NOTE: Docker build context should be the repo root (.)
# Install deps using uv into a venv NOT under /app
COPY pyproject.toml uv.lock /app/

# Tell uv where to create/use the project venv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --frozen --no-dev

# Make the venv active for all processes
ENV PATH="/opt/venv/bin:${PATH}"

# Copy your Django code after deps are installed
COPY backend/ /app/

# Make entrypoint executable (lives in /app, which is bind-mounted in dev)
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "extractable.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "90"]