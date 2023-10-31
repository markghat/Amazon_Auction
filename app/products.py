from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import jsonify

from .models.product import Product

from flask import Blueprint
bp = Blueprint('products', __name__)

# class getcount(FlaskForm):
#     user_id = IntegerField('k', validators=[InputRequired('Please enter a number!')])
#     submit = SubmitField('Insert number of most expensive items')



@bp.route('/product/expensive/', methods=['GET'])
def products_get_most_expensive():
    k = request.args.get('k', default=5, type=int)
    items = Product.get_most_expensive(k)
    return render_template('product_expensive.html',
                           avail_products=items,
                           mynum=k)

@bp.route('/sort/', methods=['GET'])
def products_filter():
    page = int(request.args.get('page', default=1))
    attribute = request.args.get('attribute', default='Most Expensive', type=str)
    if attribute == "Most Expensive":
        items = Product.get_most_expensive()
    elif attribute == "Least Expensive":
        items = Product.get_least_expensive()
    elif attribute == "Highest rating":
        items = Product.get_highest_rating()
    else:
        items = Product.get_expiration()
    return render_template('index.html',
                           avail_products=items,
                           page = page)

