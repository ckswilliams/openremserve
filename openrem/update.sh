#!/bin/bash
# Set up the postgres database for openrem
cd /usr/local/lib/python2.7/site-packages/openrem/
python manage.py makemigrations remapp
python manage.py migrate remapp
python manage.py collectstatic --noinput --clear