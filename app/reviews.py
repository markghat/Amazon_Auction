from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.review import ProductReview

from flask import Blueprint
from flask import jsonify
bp = Blueprint('reviews', __name__)


@bp.route('/reviews')
def index():
    # get all available products for sale:
    #reviews = ProductReview.get_all(True)
    # find 5 most recent reviews by current user:
    if current_user.is_authenticated:
        reviews = ProductReview.get_5_most_recent(current_user.id)
        return jsonify([review.__dict__ for review in reviews])
    else:
        return jsonify({}), 404
    # render the page by adding information to the index.html file
    
