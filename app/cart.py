from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import jsonify
from .models.product import Product
from flask import Blueprint
from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart', methods=['POST', 'GET'])
def cart():
    if request.method == 'POST' and current_user.is_authenticated:
        action = request.form.get('action', type=str)
        # Determine which action to perform
        if action == 'add':
            print("action == add so we are adding tings")
            product_id = request.form.get('product_id', type=int)
            Cart.add_to_cart(current_user.id, product_id)
        elif action == 'remove':
            Cart.remove_from_cart(current_user.id)

    _cart = []
    if current_user.is_authenticated:
        _cart = Cart.get_cart_for_user(current_user.id) 
    else:
        pass

    total_price = sum(item.product_price for item in _cart) if _cart else 0
    return render_template('cart.html',
                           cart=_cart,
                           total_price=total_price)
    

