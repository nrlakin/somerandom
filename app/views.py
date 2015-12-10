from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db, twitter, celery
from datetime import date
from .models import Post, Poster
from .forms import PostForm
from datetime import datetime, timedelta
from config import DATABASE_QUERY_TIMEOUT, USER_CREDENTIALS, MAX_TWEETS_PER_USER

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    # posts=twitter.statuses.home_timeline()
    # for post in posts:
    #     flash(post)
    form = PostForm()
    if form.validate_on_submit():
        ip = request.remote_addr
        poster = Poster.query.filter_by(ip_address=ip).first()
        if poster is None:
            poster = Poster(ip_address=ip)
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=poster)
        flash(post.body)
        db.session.add(poster)
        db.session.add(post)
        db.session.commit()
        if (verify_poster(poster)):
            flash("post is live!")
            twitter.post_status(post.body)
            #follow_back()
        else:
            flash("failed to verify poster.")
    return render_template('index.html',
                            form = form)

@celery.task(name='somerando.follow_back')
def follow_back():
    followers = get_followers()
    followed = get_followed()
    to_follow = set(followers) - set(followed)
    for user in to_follow:
        flash(follow(user).data)
        flash(user)
    return len(to_follow)

def follow(user_id):
    resp = twitter.post('friendships/create.json', data={'user_id':user_id,
        'follow':True})
    return resp

def get_followers():
    resp = twitter.get('followers/ids.json',
            data={'screen_name':USER_CREDENTIALS['twitter']['screen_name']})
    return resp.data['ids']

def get_followed():
    resp = twitter.get('friends/ids.json',
            data={'screen_name':USER_CREDENTIALS['twitter']['screen_name']})
    return resp.data['ids']

def compare_lists(a, b):
    return set(a) ^ set(b)

def verify_poster(poster):
    posts = poster.get_posts()
    if len(posts) > MAX_TWEETS_PER_USER:
        td = timedelta(days=1)
        flash(posts[MAX_TWEETS_PER_USER-1].timestamp)
        flash(datetime.utcnow() - td)
        return posts[MAX_TWEETS_PER_USER-1].timestamp < (datetime.utcnow() - td)
    return True


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
