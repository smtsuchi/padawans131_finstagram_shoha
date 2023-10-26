from flask import Flask
from config import Config
from .models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_cors import CORS

# import Blueprints
from .social import social
from .shop import shop
from .auth import auth
from .api import api

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(social)
app.register_blueprint(shop)
app.register_blueprint(auth)
app.register_blueprint(api)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
moment = Moment(app)
cors = CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = 'auth.login_page'
login_manager.login_message='Please log in to access this page!'
login_manager.login_message_category='danger'