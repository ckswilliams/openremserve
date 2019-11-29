#!/bin/bash
# Set up the postgres database for openrem
cd /app/openrem
python manage.py makemigrations remapp
python manage.py migrate --noinput
python manage.py createsuperuser
mv remapp/migrations/0002_0_7_fresh_install_add_median.py{.inactive,}
python manage.py migrate
python manage.py collectstatic --noinput --clear