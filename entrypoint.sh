#!/bin/sh

echo "⏳ Waiting for postgres..."

until pg_isready -h db -p 5432; do
  echo "Waiting for postgres..."
  sleep 1
done

echo "✅ Postgres is up - launching Flask..."
flask run --host=0.0.0.0 --port=5000
