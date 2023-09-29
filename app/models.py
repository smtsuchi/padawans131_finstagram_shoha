from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    first_name = db.Column(db.String(45))

    posts = db.relationship("Post", backref='author')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String, nullable=False)
    caption = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    likers = db.relationship("User", backref='liked_posts', secondary='like')

    def __init__(self, title, img_url, caption, user_id):
        self.title = title
        self.img_url = img_url
        self.caption = caption
        self.user_id = user_id

    def like_count(self):
        return len

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id

like = db.Table('like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False, primary_key=True),
    )

