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
SECRET_KEY = "g987Ab#nv0+"

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

# User Authentication providers
OAUTH_CREDENTIALS = {
    'github': {
        'id': 'ee5cdac30349fd80b19e',
        'secret' : '3c56b63e337e6f2bdb6b7bc6f74a6a673e2bb486'
    },
    'twitter': {
        'id': '7X5RIOTm34msy3O1hE2xsrQk3',
        'secret' : 'o5W2QOKYka2axghf1xiG6ig8K7EHVNI09mPFVPfgXjpp8FptpV'
    }
}

USER_CREDENTIALS = {
    'twitter': {
        'screen_name': 'btlakeDev',
        'access-token': '4408539945-IUwQ9JxYoG7myBO5Lz0ObeaI1mgllMq8QmoI9aS',
        'access-token-secret': 'YWVohiyvCOd2SnhM85rYNT6jIM2vrd79vNlUd2k5cFbtZ'
    }
}

MAX_TWEETS_PER_USER = 10
