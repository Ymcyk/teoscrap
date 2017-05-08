#!/bin/bash

python manage.py migrate

python manage.py scrap

exec gunicorn teoscrap.wsgi:application \
   --bind 0.0.0.0:8080 \
  --workers 3 
