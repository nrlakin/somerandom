from app import app, db

class Poster(db.Model):
    """ Class representing a single Poster; one->many Poster->Post.

    This class extends SQLAlchemy's Model class.

    Attributes:
        id (int): Unique integer primary key.
        ip_address (str): IP address from Werkzeug. Used to match poster to
            posts.
        twitter_handle (str): Twitter handle for future extension--would like to
            allow posts by reading Twitter mentions and retweeting.
        posts ([Post]): List of posts tied to this Poster.
    """
    id = db.Column(db.Integer, primary_key = True)
    ip_address = db.Column(db.String)
    twitter_handle = db.Column(db.String)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def get_posts(self):
        """List[Post]: Posts for this Poster, ordered by recency. Note that this
        function will execute a SQLAlchemy query."""
        return self.posts.order_by(Post.timestamp.desc()).all()

    def __repr__(self):
        return '<Poster %r>' % self.id

class Post(db.Model):
    """ Class representing a single Post; one->many Poster->Post.

    This class extends SQLAlchemy's Model class.

    Attributes:
        id (int): Unique integer primary key.
        body (str): Body of post. Need to define validator on Post form.
        timestamp (datetime): Time of post.
        poster_id (int): Foreign key to Poster table.
        tweet_id (integer): Twitter tweet ID, currently unused.
    """
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime)
    poster_id = db.Column(db.Integer, db.ForeignKey('poster.id'))
    tweet_id = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return '<Post %r>' % self.body
