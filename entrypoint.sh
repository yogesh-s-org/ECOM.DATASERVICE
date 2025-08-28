#!/bin/bash

# Exit on error
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."

while ! nc -z ecom-db 5432; do
  sleep 1
done

echo "PostgreSQL is up. Running migrations..."

# Run migrations
python manage.py migrate

# Collect static files (optional)
# python manage.py collectstatic --noinput

# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000
