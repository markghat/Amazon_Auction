from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import jsonify

from .models.product import Product
from .models.review import ProductReview

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


@bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_info(product_id):
    if not current_user.is_authenticated:
        return redirect(url_for('index.index'))
    # Replace this with code to fetch product information from your database based on product_id
    product = Product.get(product_id)
    product_reviews = ProductReview.get_by_pid(product_id)
    total_reviews = ProductReview.get_total_number_by_id(product_id)
    avg_rating = ProductReview.get_average_rating(product_id)
    my_review = ProductReview.get_last_review(product_id, current_user.id)

    # if request.method == 'POST':
    #     # Handle bid submission here
    #     bid_amount = float(request.form.get('bidAmount'))
    #     # Process the bid and update the current bid in your database

    return render_template('product_info.html',
                           isNewReview=my_review is None, 
                           my_review=my_review,
                           product=product, 
                           product_reviews=product_reviews, 
                           total=total_reviews, 
                           average=avg_rating)
