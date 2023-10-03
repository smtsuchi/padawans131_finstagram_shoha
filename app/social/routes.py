from . import social
from flask import redirect, render_template, request, url_for, flash
from .forms import PostForm
from ..models import db, User, Post
from flask_login import current_user, login_required
from datetime import datetime

## Instagram
@social.route('/posts/create', methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            #create a post for the logged in user
            post = Post(title, img_url, caption, current_user.id)

            db.session.add(post)
            db.session.commit()
            flash('Successfully created your post.', 'success')
            return redirect(url_for('social.feed'))
    return render_template('create-post.html', form=form)

@social.route('/')
@social.route('/posts')
def feed():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('feed.html', posts=posts)

@social.route('/posts/<post_id>')
def individual_post_page(post_id):
    post = Post.query.get(post_id)
    # post = Post.query.filter_by(id=post_id).first()
    
    return render_template('individual-post.html', p=post)

@social.route('/posts/update/<post_id>', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('That post does not exist', 'danger')
        return redirect(url_for('social.feed'))
    if current_user.id != post.user_id:
        flash('You cannot edit another user\'s posts', 'danger')
        return redirect(url_for('social.individual_post_page', post_id=post_id))
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post.title = title
            post.img_url = img_url
            post.caption = caption
            post.last_updated = datetime.utcnow()

            db.session.commit()
            flash('Successfully updated your post.', 'success')
            return redirect(url_for('social.individual_post_page', post_id=post_id))
    return render_template('update-post.html', p=post, form = form)

@social.route('/posts/delete/<post_id>', methods=["GET"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('That post does not exist', 'danger')
        return redirect(url_for('social.feed'))
    if current_user.id != post.user_id:
        flash('You cannot delete another user\'s posts', 'danger')
        return redirect(url_for('social.individual_post_page', post_id=post_id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted your post', 'success')
    return redirect(url_for('social.feed'))

@social.route('/like/<post_id>')
@login_required
def like(post_id):
    post = Post.query.get(post_id)
    if post:
        print(post.likers)
        post.likers.append(current_user)
        db.session.commit()
    return redirect(url_for('social.individual_post_page', post_id=post_id))

@social.route('/unlike/<post_id>')
@login_required
def unlike(post_id):
    post = Post.query.get(post_id)
    if post:
        print(post.likers)
        post.likers.remove(current_user)
        db.session.commit()
    return redirect(url_for('social.individual_post_page', post_id=post_id))

@social.route('/people')
@login_required
def people_page():
    users = User.query.order_by(User.username).filter(User.username != current_user.username).all()
    current_user.get_following()
    return render_template('people.html', users=users)

@social.route('/follow/<user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.following.append(user)
        db.session.commit()
    return redirect(url_for('social.people_page'))

@social.route('/unfollow/<user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.following.remove(user)
        db.session.commit()
    return redirect(url_for('social.people_page'))