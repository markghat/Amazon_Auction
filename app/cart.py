from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def index():
    
    # find the products current user has bought:
    if not current_user.is_authenticated:
        return redirect('index/')
    else:
        cart = Cart.get_all_by_user_id(current_user.id)
    # render the page by adding information to the index.html file
    return render_template('cart.html',
                           cart_items=cart)
