#!/bin/bash

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

exec gunicorn server.wsgi:application --bind 0.0.0.0:"${DJANGO_PORT}" --reload