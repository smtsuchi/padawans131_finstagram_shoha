from . import api
from ..models import db, Post
from flask import request

@api.get('/posts')
def all_posts_api():
    posts = Post.query.order_by(Post.date_created.desc()).all() # list of Post Objects
    posts = [p.to_dict() for p in posts] # list of Post Dictionaries
    return {
        'status':'ok',
        'total_results': len(posts),
        'posts': posts
    }

@api.get('/posts/<post_id>')
def single_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'total_results': 1,
            'post': post.to_dict()
        }
    return {
        'status': 'not ok',
        'message': 'A post with that ID does not exist.'
    }, 404

@api.post('/posts/create')
def create_post_api():
    data = request.json
    title = data['title']
    caption = data['caption']
    img_url = data['img_url']
    user_id = data['user_id']

    post = Post(title, img_url, caption, user_id)

    db.session.add(post)
    db.session.commit()

    return {
        'status': 'ok',
        'message': "Successfully created the post."
    }, 201

