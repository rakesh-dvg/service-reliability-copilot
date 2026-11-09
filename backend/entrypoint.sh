#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Seeding demo data (idempotent)..."
python -m app.seed || true

echo "Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
