# ================================
# Stage 1: Build dependencies
# ================================
FROM python:3.11-slim AS builder

WORKDIR /app

# System dependencies for MySQL + build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install pip tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install in a virtual env
COPY requirements.txt .
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ================================
# Stage 2: Runtime
# ================================
FROM python:3.11-slim

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN addgroup --system django && adduser --system --ingroup django django

# Copy only necessary files (avoid .git, docs, etc.)
COPY . .

# Set ownership
RUN chown -R django:django /app

USER django

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run Gunicorn as default entrypoint
CMD ["gunicorn", "Library_Management.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3", "--timeout=120"]
