FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Bra defaults för Python i containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Installera dependencies först (cache-vänligt)
COPY pyproject.toml uv.lock ./
COPY src/brottsbalken/backend/pyproject.toml src/brottsbalken/backend/pyproject.toml
COPY src/brottsbalken/frontend/pyproject.toml src/brottsbalken/frontend/pyproject.toml
COPY src/brottsbalken/monitoring/pyproject.toml src/brottsbalken/monitoring/pyproject.toml

RUN uv sync --frozen

# Kopiera resten av projektet
COPY . .

EXPOSE 8000 8501 5001