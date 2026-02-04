#!/usr/bin/env bash
set -o errexit

echo "==> Install dependencies"
pip install -r requirements.txt

echo "==> Collect static"
python manage.py collectstatic --noinput

echo "==> Migrate database"
python manage.py migrate --noinput
