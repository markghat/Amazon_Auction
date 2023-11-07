from flask import render_template, request, abort
from flask import redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.review import ProductReview

from flask import Blueprint
from flask import jsonify
bp = Blueprint('reviews', __name__)


#Form for finding 5 most recent reviews
class findReview(FlaskForm):
    user_id = IntegerField('User_ID', validators=[InputRequired('Please enter a user id!')])
    submit = SubmitField('Find 5 most recent reviews!')


@bp.route('/reviews', methods=['POST', 'GET'])
def index():

    form = findReview()
    if form.validate_on_submit():
        uid = form.user_id.data
        return redirect('reviews/'+str(uid))
    if current_user.is_authenticated:
        reviews = ProductReview.get_all()
        myReviews = ProductReview.get_by_uid(current_user.id)
        return render_template('reviews.html', all_reviews=reviews, my_reviews=myReviews, form=form)
    else:
        reviews = ProductReview.get_all()
        return render_template('reviews.html', all_reviews=reviews, form=form)

@bp.route('/reviews/<int:uid>', methods=['POST', 'GET'])
def fiveRecent(uid):
    if current_user.is_authenticated:
        reviewsbysoso = ProductReview.get_5_most_recent(uid)
        myReviews = ProductReview.get_by_uid(current_user.id)
        reviews = ProductReview.get_all()
        return render_template('5reviews.html', soso_reviews=reviewsbysoso,all_reviews=reviews, my_reviews=myReviews)
    else:
        reviewsbysoso = ProductReview.get_5_most_recent(uid)
        reviews = ProductReview.get_all()
        return render_template('5reviews.html', soso_reviews=reviewsbysoso,all_reviews=reviews)
        

# @bp.route('/addReview', methods=['GET', 'POST'])
# def addReview():
#     if not current_user.is_authenticated:
#         return redirect(url_for('index.index'))

#     pid = request.args.get('id')
#     previous_review = ProductReview.get_last_review(pid, current_user.id)

#     # Handle the post request
#     if request.method == 'POST':
#         ProductReview.add(current_user.id, pid, request.form['rating'], request.form['comment'])
        
#         return redirect(url_for('reviews.review'))
#     return render_template('addOrUpdateReview.html', isNewReview=previous_review is None, previous_review=previous_review)


# @bp.route('/reviews/add/<int:product_id>', methods=['POST', 'GET'])
# def addReview():
#     if not current_user.is_authenticated:
#         return redirect(url_for('index.index'))
#     if current_user.is_authenticated:
#         reviews = ProductReview.get_5_most_recent(current_user.id)
#         return jsonify([review.__dict__ for review in reviews])
#     # Handle the post request
#     if request.method == 'POST':
#         ProductReview.add(current_user.id,
#                             product_id,
#                             request.form['rating'],
#                             request.form['comment'])
#         return redirect(url_for('reviews.review'))
#     else:
#         return jsonify({}), 404
    
