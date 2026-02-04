#!/usr/bin/env bash
set -o errexit

echo "==> Install dependencies"
pip install -r requirements.txt

echo "==> Run database migrations"
python manage.py migrate --noinput

echo "==> Collect static files"
python manage.py collectstatic --noinput
