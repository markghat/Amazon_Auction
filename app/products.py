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


@bp.route('/product/expensive/<int:k>', methods=['GET'])
def products_get_most_expensive(k):
    items = Product.get_most_expensive(k)
    return render_template('product_expensive.html',
                           avail_products=items,
                           mynum=k)

