#!/bin/bash
echo "Starting IntlQ..."
export DEBUG=False
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:5000 --workers 2 "app:create_app()"
