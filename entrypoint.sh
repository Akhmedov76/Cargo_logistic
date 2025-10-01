#!/bin/sh

# DB tayyor bo'lishini kutish
echo "Waiting for Postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "Postgres is up - continuing..."

# Django migratsiyalarini bajarish
echo "Applying migrations..."
python manage.py migrate --noinput

# Static fayllarni collect qilish
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Daphne serverini ishga tushirish
echo "Starting Daphne server..."
daphne conf.asgi:application -b 0.0.0.0 -p 7009
