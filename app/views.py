from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db, twitter
from datetime import date
from .models import Poster
from .emails import follower_notification
from datetime import datetime
from config import DATABASE_QUERY_TIMEOUT
from oauthsignin import OAuthSignIn

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    resp=twitter.get('users/lookup.json', data={'screen_name':self.screen_name}).data
    flash(resp)
    return render_template('index.html')

@twitter.tokengetter
def get_token(self):
    cred = current_app.config[USER_CREDENTIALS]
    return (cred['access-token'], cred['access-token-secret'])

@app.before_request
def before_request():
    pass

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Error-404'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='Error-500')

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\n Context: %s\n" %
                (query.statement, query.parameters, query.duration, query.context))
    return response
