from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase


from .models.sells import SoldItem

from .models.user import User


from flask import Blueprint
bp = Blueprint('index', __name__) #changed to purchased


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


    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)



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

@bp.route('/sells/inventory', methods = ['GET'])
def seller_inventory():
    #charityId = request.args.get('charityId', default=5, type=int)
    #print("in function")
    
    #items = SoldItem.get_charity_items(int(charityId))

    if current_user.is_authenticated and User.isCharity(current_user.id):
        # WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
        # return redirect(url_for('wishlist.wishlist'))

        charityId = User.getCharityId(currrent_user.id) # TO DO: Need to make sure that this can be cast as an int

        
        items = SoldItem.get_charity_items(int(charityId))

        return render_template('seller_inventory.html', 
        avail_products = items,
        mynum= charityId)
    else:
        return redirect(url_for('index.sells'))


    # return render_template('seller_inventory.html', 
    # avail_products = items,
    # mynum= charityId)


@bp.route('/sells/inventory/remove/<int:product_id>', methods=['POST'])
def sells_remove(product_id):
    #Purchase.add_purchase(current_user.id, product_id, datetime.datetime.now()) #how to get the current time
    SoldItem.remove_charity_item(product_id)
    return redirect(url_for('index.sells'))



