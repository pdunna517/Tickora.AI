#!/bin/bash

# Render deployment startup script
# Reads PORT from environment variable (Render provides this)
# Defaults to 10000 if not set

PORT=${PORT:-10000}

echo "Starting Tickora API on port $PORT..."

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
