web: gunicorn app:app
worker: celery -A app.celery.celery worker -B --loglevel=info
