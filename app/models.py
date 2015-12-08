from app import app, db

class Poster(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ip_address = db.Column(db.String)
    twitter_handle = db.Column(db.String)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime)
    poster_id = db.Column(db.Integer, db.ForeignKey('poster.id'))
    tweet_id = db.Column(db.Integer, nullable = True)
