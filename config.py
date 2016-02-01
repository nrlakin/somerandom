"""
Sample config file for Flask app; if you are using this to build your own app,
your changes will go here.  Do not post this on github if it contains real keys!
"""

import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'somerando.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5

WTF_CSRF_ENABLED = True
if os.environ.get('CSRF_SECRET') is None:
    SECRET_KEY = "tough secret"
else:
    CSRF_SECRET = os.environ.get('CSRF_SECRET')

# Mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

ADMINS = ['neil.lakin.dev@gmail.com']

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = {
    'update_followers': {
        'task': 'somerandom.follow_back',
        'schedule' : timedelta(seconds=30),
        'args' : ()
    }
}

USER_CREDENTIALS = {
    'twitter': {
        'screen_name': os.environ.get('TWITTER_HANDLE'),
        'access-token': os.environ.get('TWITTER_ACCESS_TOKEN'),
        'access-token-secret': os.environ.get('TWITTER_TOKEN_SECRET')
    }
}

MAX_TWEETS_PER_USER = 10
