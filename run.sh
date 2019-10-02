#!/bin/bash
python manage.py migrate --noinput
gunicorn -b 0.0.0.0:8080 black_tom.wsgi
