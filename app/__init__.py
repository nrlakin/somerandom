from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask_oauthlib.client import OAuth
from flask.ext.mail import Mail
from celery_config import make_celery
from twitterclient import TwitterClient
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
#app = Flask("somerandom")

app.config.from_object('config')
db = SQLAlchemy(app)
oauth = OAuth(app)
celery = make_celery(app)

# Set up email logging
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' +
                                MAIL_SERVER, ADMINS, 'rando error', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# Set up log file.
if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/rando.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('SomeRandom startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('SomeRandom startup')

twitter = TwitterClient(
    oauth,
    'twitter',
    consumer_key=app.config['OAUTH_CREDENTIALS']['twitter']['id'],
    consumer_secret=app.config['OAUTH_CREDENTIALS']['twitter']['secret'],
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    user_credentials=app.config['USER_CREDENTIALS']['twitter'],
    logger=app.logger
)


from app import views, models
