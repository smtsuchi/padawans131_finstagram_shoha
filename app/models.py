from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from secrets import token_hex

db = SQLAlchemy()

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), nullable=False)
    )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    first_name = db.Column(db.String(45))
    token = db.Column(db.String, unique=True)
    
    posts = db.relationship("Post", backref='author')
    following = db.relationship(
        'User',
        backref='followers',
        secondary='followers',
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id)
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.token = token_hex(16)

    def get_following(self):
        following_set = {u.id for u in self.following}
        return following_set

    def follows(self, user):
        return user.id in self.get_following()
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'date_created': self.date_created,
            'first_name': self.first_name,
            'token': self.token,
            'follower_count': len(self.followers),
            'following_count': len(self.following),
        }


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
        return len(self.likers)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'caption': self.caption,
            'img_url': self.img_url,
            'user_id': self.user_id,
            'author': self.author.username,
            'date_created': self.date_created,
            'last_updated': self.last_updated,
            'like_count': self.like_count(),
        }


like = db.Table('like',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False, primary_key=True),
    )

# class Like(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

#     def __init__(self, user_id, post_id):
#         self.user_id = user_id
#         self.post_id = post_id
