#!/bin/bash
python manage.py migrate --noinput
gunicorn -b 0.0.0.0:8080 black_tom.wsgi --log-level debug --timeout 150 --workers 2 -k gevent
