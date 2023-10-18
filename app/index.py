from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase


from .models.sells import SoldItem

from flask import Blueprint
bp = Blueprint('index', __name__) #changed to purchased
from humanize import naturaltime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/')
def index():
    
    # get all available products for sale:
    products = Product.get_all(True)

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file

    #print("At homepage, this is the type of the products" + str(type(products)))
    #print("At homepage, this is the type of the purchases" + str(type(purchases)))
    print("At homepage, this is the type of a purchase item" + str(type(products[0])))


    return render_template('index.html', #change to purchased.html and add humanize
                           avail_products=products,
                           purchase_history=purchases,
                           humanize_time=humanize_time
                            )



@bp.route('/sells/', methods = ['GET'])
def sells():
    charityId = request.args.get('charityId', default=5, type=int)
    print("in function")
    
    items = SoldItem.get_charity_items(int(charityId)) # array of 

    # print(type(items[0]))
    # print("items is " + str(items[0]))

    #items = [row[0] for row in items] # list of strings

    #for item in items:
     #   print(item)

    # need to convert items to type list

    return render_template('seller_products.html', 
    avail_products = items,
    mynum= charityId)

