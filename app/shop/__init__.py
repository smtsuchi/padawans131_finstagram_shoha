from flask import Blueprint

shop = Blueprint('shop', __name__, template_folder='shop_templates')

from . import routes