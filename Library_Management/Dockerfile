FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install pip tools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Security: run as non-root user
RUN addgroup --system django && adduser --system --ingroup django django
RUN chown -R django:django /app
USER django

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Entrypoint and default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "Library_Management.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3", "--timeout=120"]
