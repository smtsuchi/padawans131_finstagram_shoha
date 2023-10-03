from flask import Blueprint

social = Blueprint('social', __name__, template_folder='social_templates')

from . import routes