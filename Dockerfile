# =========================================================
# STAGE 1 — BUILDER
# =========================================================
FROM python:3.12-slim AS builder

# =========================================================
# ENVIRONMENT
# =========================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# =========================================================
# WORKDIR
# =========================================================
WORKDIR /build

# =========================================================
# SYSTEM DEPENDENCIES
# =========================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libc6-dev \
    libpq-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================================================
# VIRTUAL ENVIRONMENT
# =========================================================
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# =========================================================
# INSTALL DEPENDENCIES
# =========================================================
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

# =========================================================
# STAGE 2 — RUNTIME
# =========================================================
FROM python:3.11-slim AS runtime

# =========================================================
# ENVIRONMENT
# =========================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    PATH="/opt/venv/bin:$PATH"

# =========================================================
# WORKDIR
# =========================================================
WORKDIR /app

# =========================================================
# RUNTIME DEPENDENCIES
# =========================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================================================
# COPY VENV
# =========================================================
COPY --from=builder /opt/venv /opt/venv

# =========================================================
# COPY PROJECT
# =========================================================
COPY . .

# =========================================================
# CREATE NON-ROOT USER
# =========================================================
RUN useradd -m appuser

RUN chown -R appuser:appuser /app

USER appuser

# =========================================================
# HEALTHCHECK
# =========================================================
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# =========================================================
# EXPOSE
# =========================================================
EXPOSE 8501

# =========================================================
# START APP
# =========================================================
CMD ["streamlit", "run", "app.py"]
