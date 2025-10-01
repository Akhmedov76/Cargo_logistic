#!/bin/sh

echo "Waiting for Postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Postgres not ready, sleeping 1s..."
  sleep 1
done
echo "Postgres is up - continuing..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

daphne conf.asgi:application -b 0.0.0.0 -p 7009
