#!/usr/bin/env bash
set -e

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py makemigrations erp
python manage.py migrate --noinput

python manage.py ensure_admin
