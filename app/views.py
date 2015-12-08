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

@app.route('/login', methods=['GET','POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login_oauth.html',
                            title = 'Sign In',
                            providers = app.config['OAUTH_CREDENTIALS'])

# @app.route('/login', methods=['GET','POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None and g.user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#                     (form.openid.data, str(form.remember_me.data)))
#         return oid.try_login(form.openid.data, ask_for=['nickname','email'])
#     return render_template('login.html',
#                             title = 'Sign In',
#                             form = form,
#                             providers = app.config['OPENID_PROVIDERS'])

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('oauth_token', None)
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                            user = user,
                            posts= posts)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself.')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Can\'t follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '.')
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself.')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Can\'t unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                            query=query,
                            results=results)

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == '':
        flash('Invalid login. Try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        social_id = '$'.join(['email', email])
        user = User(nickname=nickname, social_id = social_id, email=resp.email)
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
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form=SearchForm()

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

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
