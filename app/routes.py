from app import app
from flask import redirect, render_template, request, url_for
from .forms import LoginForm, SignUpForm, PostForm
from .models import db, User, Post
from flask_login import login_user, logout_user, current_user, login_required

@app.route("/")
def index():
    return render_template('index.html')

## Authentication

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if request.method == 'POST':
        print("POST REQUEST MADE!")
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # does a user with that username already exist?
            # does a user with that email already exist?

            user = User(username, email, password)
            
            db.session.add(user)
            db.session.commit()


        else:
            print("FORM INVALID! :(")

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
                else:
                    print('passwords dont match')
            else:
                print('that user doesnt exist')

        return redirect(url_for('index'))
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

            return redirect(url_for('index'))
    return render_template('create-post.html', form=form)

@app.route('/posts')
def feed():
    posts = Post.query.all()
    print(posts)
    return render_template('feed.html', posts=posts)