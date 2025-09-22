#!/bin/bash
set -e

echo "🚀 Starting Django entrypoint script..."

# Wait for database to be ready
echo "⏳ Waiting for database..."
until python manage.py migrate --noinput; do
  echo "⚠️  Database not ready, retrying in 5s..."
  sleep 5
done

# Run migrations explicitly (just in case schema changed)
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "✅ All setup complete, launching Gunicorn..."

# Exec the CMD from Dockerfile (Gunicorn)
exec "$@"
