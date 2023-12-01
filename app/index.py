from flask import render_template, request, url_for
from flask_login import login_user, logout_user, current_user
import datetime
from flask import request, jsonify

from flask import redirect, flash


from .models.product import Product
from .models.purchase import Purchase
from .models.order import Order


from .models.sells import SoldItem

from .models.user import User


from flask import Blueprint
bp = Blueprint('index', __name__) #changed to purchased
from humanize import naturaltime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/')
def index():
    
    # get all available products for sale:
    products = Product.get_all(True)
    page = int(request.args.get('page', default=1))
    

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file

    #print("At homepage, this is the type of the products" + str(type(products)))
    #print("At homepage, this is the type of the purchases" + str(type(purchases)))
    #print("At homepage, this is the type of a purchase item" + str(type(products[0])))

    return render_template('index.html', #change to purchased.html and add humanize
                           avail_products=products,
                           purchase_history=purchases,
                           humanize_time=humanize_time,
                           page=page)



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

    #if current_user.is_authenticated: #and User.isCharity(current_user.id):
    if current_user.is_authenticated and User.isCharity(current_user.id):
        # WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
        # return redirect(url_for('wishlist.wishlist'))

        print(current_user.id)

        charityId = User.getCharityId(current_user.id) # TO DO: Need to make sure that this can be cast as an int


        name = User.getCharityName(current_user.id)
        
        items = SoldItem.get_charity_items(int(charityId))

        return render_template('seller_inventory.html', 
        avail_products = items,
        mynum= charityId,
        charityName = name)
    else:
        return redirect(url_for('index.index'))


    # return render_template('seller_inventory.html', 
    # avail_products = items,
    # mynum= charityId)

@bp.route('/sells/orders', methods = ['GET', 'POST'])
def seller_orders():
    #charityId = request.args.get('charityId', default=5, type=int)
    #print("in function")
    
    #items = SoldItem.get_charity_items(int(charityId))

    #if current_user.is_authenticated: #and User.isCharity(current_user.id):
    if current_user.is_authenticated and User.isCharity(current_user.id):
        # WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
        # return redirect(url_for('wishlist.wishlist'))

        print(current_user.id)

        charityId = User.getCharityId(current_user.id) # TO DO: Need to make sure that this can be cast as an int


        name = User.getCharityName(current_user.id)
        
        #items = SoldItem.get_charity_items(int(charityId))
        items = SoldItem.get_charity_orders(int(charityId))


        if request.method == 'POST':

            print("value of status before if statement")
            print(request.form['order_status'])
            #newStatus = bool(request.form['order_status'])
            newStatus = request.form['order_status']
            print(newStatus)
            
            if newStatus == "True": 
                newStatus = False
            else: 
                newStatus = True

            #newStatus = not request.form['order_status']
            print("value of newStatus in seller_orders()")
            print(newStatus)
            Order.change_fulfillment_status(request.form['order_id'],newStatus)
            items = SoldItem.get_charity_orders(int(charityId))

        return render_template('seller_orders.html', 
        avail_orders = items,
        mynum= charityId,
        charityName = name)
    else:
        return redirect(url_for('index.index'))


@bp.route('/sells/inventory/remove/<int:product_id>', methods=['POST'])
def sells_remove(product_id):
    #Purchase.add_purchase(current_user.id, product_id, datetime.datetime.now()) #how to get the current time
    SoldItem.remove_charity_item(product_id)
    return redirect(url_for('index.seller_inventory'))

@bp.route('/sells/inventory/add/', methods=['POST'])
def sells_add():

    print("reached sells_add method")

    # Retrieving form data:
    name = request.form.get('name', default='', type=str)
    price = request.form.get('price', default=0.0, type=float)
    category = request.form.get('category', default='', type=str)
    #expiration_str = request.form.get('expiration', default='', type=str)
    image = request.form.get('image', default='', type=str)

    # Retrieve separate expiration date components
    expiration_month_name = request.form.get('expiration_month', default='', type=str)
    expiration_day = request.form.get('expiration_day', default='', type=str)
    expiration_year = request.form.get('expiration_year', default='', type=str)
    
    # Retrieve expiration time
    expiration_time = request.form.get('expiration_time', default='', type=str)

    
    # Validate the form data (might remove this if statement altogether??)
    if not name or not price or not expiration_month_name or not expiration_day or not expiration_year or not expiration_time:
        flash('Name, price, and expiration details are required fields.', 'error')
        return redirect(url_for('index.seller_inventory'))

    month_name_to_number = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09',
    'October': '10',
    'November': '11',
    'December': '12'
    }

    # Convert the month name to the corresponding number
    expiration_month = month_name_to_number.get(expiration_month_name)
    if not expiration_month:
        flash('Invalid month name.', 'error')
        return redirect(url_for('index.seller_inventory'))

    # Combine expiration components into a string
    expiration_str = f"{expiration_year}-{expiration_month}-{expiration_day} {expiration_time}"

    #expiration_dt = datetime.strptime(expiration_str, '%Y-%m-%d %H:%M:%S.%f')
    expiration_dt = datetime.datetime.strptime(expiration_str, '%Y-%m-%d %H:%M:%S')


    charityId = User.getCharityId(current_user.id) # TO DO: Need to make sure that this can be cast as an int

    SoldItem.add_charity_item(charityId, name, price, category, expiration_dt, image)


    #SoldItem.add_charity_item(int(charityId), str(name), price, category, expiration, image)
    #SoldItem.add_charity_item(0, 5.50,"broski??????")

    return redirect(url_for('index.seller_inventory'))


# @bp.route('/changeorderstatus', methods=['POST'])
# def seller_change_order_status():
#     data = request.get_json()
#     order_id = data.get('orderId')
#     is_checked = data.get('isChecked')

#     app.db.execute('''
#         UPDATE Orders
#         SET status = :is_checked
#         WHERE id = :order_id
#     ''', is_checked=is_checked, order_id=order_id)

#     return redirect(url_for('index.seller_orders'))
