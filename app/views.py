from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db, oauth
from datetime import date
from .models import Poster
from .emails import follower_notification
from datetime import datetime
from config import DATABASE_QUERY_TIMEOUT
from oauthsignin import OAuthSignIn

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                title = 'Home',
                form = form,
                posts = posts)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    signin = OAuthSignIn.get_provider(provider)
    return signin.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    signin = OAuthSignIn.get_provider(provider)
    resp = signin.authorized_response()
    if resp is None:
        flash('Access denied: %s\n%s' % (
                request.args['error'],
                request.args['error_description']),
                 'error')
        return render_template('500.html', title='Error-500')
    signin.store_token(resp)
    user_name = signin.get_username()
    social_id = '$'.join([provider, user_name])
    user = User.query.filter_by(social_id=social_id).first()
    if user is None:
        nickname = user_name
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, social_id=social_id)
        flash("Creating account: nickname=%s\nsocial_id=%s\n" % (
            nickname, social_id)
        )
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me=False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

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
