from . import auth
from flask import redirect, render_template, request, url_for, flash
from .forms import LoginForm, SignUpForm
from ..models import db, User
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
## Authentication
@auth.route("/signup", methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('social.feed'))
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
            return redirect(url_for('auth.login_page'))
        else:
            flash("Invalid form. Please try again.", 'error')

    return render_template('signup.html', form=form)

@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('social.feed'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            # Look in the database for a user with that username
            user = User.query.filter_by(username=username).first() 
            # if they exist, see if the password match
            if user:
                if check_password_hash(user.password, password):
            # if passwords match, consider them logged in
                    login_user(user)
                    flash('Successfully logged in.', 'success')
                    return redirect(url_for('social.feed'))
                else:
                    flash('Incorrect username/password combination.', 'danger')
            else:
                flash('That username does not exist.', 'danger')
    return render_template('login.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))

