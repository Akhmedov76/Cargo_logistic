#!/bin/sh

# DB tayyor bo'lishini kutish
echo "Waiting for Postgres..."
while ! (echo > /dev/tcp/$DB_HOST/$DB_PORT) 2>/dev/null; do
  sleep 1
done
echo "Postgres is up - continuing..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput
daphne conf.asgi:application -b 0.0.0.0 -p 7009
