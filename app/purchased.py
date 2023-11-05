from flask import render_template
from flask_login import current_user
import datetime
from flask import redirect, url_for

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('purchased', __name__) #changed to purchased

from humanize import naturaltime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)


@bp.route('/purchased')
def purchased():
    # get all available products for sale:
    products = Product.get_all(True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('purchased.html', #change to purchased.html and add humanize
                           avail_products=products,
                           purchase_history=purchases,
                           humanize_time=humanize_time
                            )

@bp.route('/purchased/add/<int:product_id>', methods=['POST'])
def purchased_add(product_id):
    if current_user.is_authenticated and current_user.balance > Product.getPrice(product_id):
        Purchase.add_purchase(current_user.id, product_id, datetime.datetime.now()) #how to get the current time
        return redirect(url_for('purchased.purchased'))
    else:
        return redirect(url_for('users.updateBalance'))