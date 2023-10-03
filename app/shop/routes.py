from . import shop
from flask import render_template


## Shop routes
@shop.route('/shop', methods=["GET", "POST"])
def shop_page():
    return render_template('shop.html')