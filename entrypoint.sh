#!/bin/sh
# entrypoint.sh

# Django migratsiyalarini bajarish
echo "Applying database migrations..."
python manage.py migrate --noinput

# Static fayllarni collect qilish (agar kerak bo'lsa)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Daphne serverini ishga tushirish
echo "Starting Daphne server..."
daphne conf.asgi:application -b 0.0.0.0 -p 7009
