from app import app
from flask import redirect, render_template, request, url_for, flash
from .forms import LoginForm, SignUpForm, PostForm
from .models import db, User, Post
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

## Authentication

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # does a user with that username already exist?
            # does a user with that email already exist?

            user = User(username, email, password)
            
            db.session.add(user)
            db.session.commit()

            flash('Successfully created your account. Sign in now.', "success")
        else:
            flash("Invalid form. Please try again.", 'error')

    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            # Look in the database for a user with that username
            user = User.query.filter_by(username=username).first() 
            # if they exist, see if the password match
            if user:
                if user.password == password:
            # if passwords match, consider them logged in
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('feed'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('That username does not exist.', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_page'))

## Instagram
@app.route('/posts/create', methods=["GET", "POST"])
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
            return redirect(url_for('feed'))
    return render_template('create-post.html', form=form)

@app.route('/')
@app.route('/posts')
def feed():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('feed.html', posts=posts)

@app.route('/posts/<post_id>')
def individual_post_page(post_id):
    post = Post.query.get(post_id)
    # post = Post.query.filter_by(id=post_id).first()
    
    return render_template('individual-post.html', p=post)

@app.route('/posts/update/<post_id>', methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('That post does not exist', 'danger')
        return redirect(url_for('feed'))
    if current_user.id != post.user_id:
        flash('You cannot edit another user\'s posts', 'danger')
        return redirect(url_for('individual_post_page', post_id=post_id))
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
            return redirect(url_for('individual_post_page', post_id=post_id))
    return render_template('update-post.html', p=post, form = form)

@app.route('/posts/delete/<post_id>', methods=["GET"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('That post does not exist', 'danger')
        return redirect(url_for('feed'))
    if current_user.id != post.user_id:
        flash('You cannot delete another user\'s posts', 'danger')
        return redirect(url_for('individual_post_page', post_id=post_id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted your post', 'success')
    return redirect(url_for('feed'))

@app.route('/like/<post_id>')
@login_required
def like(post_id):
    post = Post.query.get(post_id)
    if post:
        print(post.likers)
        post.likers.append(current_user)
        db.session.commit()
    return redirect(url_for('individual_post_page', post_id=post_id))

@app.route('/unlike/<post_id>')
@login_required
def unlike(post_id):
    post = Post.query.get(post_id)
    if post:
        print(post.likers)
        post.likers.remove(current_user)
        db.session.commit()
    return redirect(url_for('individual_post_page', post_id=post_id))