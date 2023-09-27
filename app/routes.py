from app import app
from flask import render_template, request
from .forms import LoginForm, SignUpForm
from .models import db, User

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def signup_page():
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


def get_pokemon(name):
    if name=='pikachu':
        return {
            'name': 'Pikachu',
            'ability': "Thunder Shock"
        }

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data

            small_dictionary = get_pokemon(username)

            # Look in the database for a user with that username
            # if they exist, see if the password match
            # if passwords match, consider them logged in

        return render_template('login.html', form = form, pokemon=small_dictionary)
    return render_template('login.html', form = form)










