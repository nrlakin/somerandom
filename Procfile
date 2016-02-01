web: gunicorn app:app
worker: celery worker --app=app.celery
init: python db_create.py
upgrade: python db_upgrade.py
