web: gunicorn app:app
worker: celery worker --app=app.app
init: python db_create.py
upgrade: python db_upgrade.py
