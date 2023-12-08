from flask import current_app, Flask, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
import datetime
from flask import request, jsonify
from flask_mail import Mail, Message
from .models.charity import Charity



from flask import redirect, flash


from .models.product import Product
from .models.purchase import Purchase
from .models.order import Order
from .models.sells import SoldItem


from .models.sells import SoldItem

from .models.user import User


from flask import Blueprint
bp = Blueprint('index', __name__) #changed to purchased
from humanize import naturaltime
from app import mail  # import the mail instance


def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

def apply_filters(products, category_filter, price_range_filter):
    # Implement filter logic
    filtered_products = products
    # Apply category filter
    if category_filter and category_filter != 'All Categories':
        filtered_products = [product for product in filtered_products if product.catergory == category_filter]

    # Apply price range filter
    if price_range_filter:
        min_price, max_price = map(int, price_range_filter.split('-'))
        filtered_products = [product for product in filtered_products if min_price <= product.price <= max_price]

    return filtered_products


@bp.route('/charities')
def list_charities():
    # Logic to retrieve all charities
    page = int(request.args.get('page', default=1))
    charities = Charity.get_all()
    print(charities[0].name)
    print('woahhhh')
    return render_template('charities.html', charities=charities, page=page)

@bp.route('/charities/search', methods=['GET'])
def search_charities():
    search_query = request.args.get('search_query')
    page = int(request.args.get('page', default=1))
    # Implement search logic (e.g., by name)
    results = Charity.search_by_name(search_query)
    return render_template('charities.html', charities=results,
                           page=page)

@bp.route('/')
def index():
    
    # get all available products for sale:
    products = Product.get_all(True)

    # Retrieve the selected category filter and price range filter from the URL
    category_filter = request.args.get('category', default='', type=str)
    price_range_filter = request.args.get('priceRange', default='', type=str)

    # Apply the filters to the products based on the selected category and price range
    filtered_products = apply_filters(products, category_filter, price_range_filter)


    page = int(request.args.get('page', default=1))
    

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('welcome.html', #change to purchased.html and add humanize
                           avail_products=filtered_products,
                           purchase_history=purchases,
                           humanize_time=humanize_time,
                           page=page)

#displays all available products for sale with an option to filter by price, rating etc
@bp.route('/products')
def products():
        # get all available products for sale:
    products = Product.get_all(True)

    # Retrieve the selected category filter and price range filter from the URL
    category_filter = request.args.get('category', default='', type=str)
    price_range_filter = request.args.get('priceRange', default='', type=str)

    # Apply the filters to the products based on the selected category and price range
    filtered_products = apply_filters(products, category_filter, price_range_filter)


    page = int(request.args.get('page', default=1))
    

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html', #change to purchased.html and add humanize
                           avail_products=filtered_products,
                           purchase_history=purchases,
                           humanize_time=humanize_time,
                           page=page)


#searches the products/sellers based on a given search query
@bp.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    search_type = request.args.get('search_type')
    page = int(request.args.get('page', default=1))
    # Add logic to handle the search query based on the search type
    if search_type == 'product':
        # Search products by name or other attributes
        results = Product.search_by_name(search_query)
    elif search_type == 'seller':
        # Search sellers by name or other attributes
        results = SoldItem.search_by_seller(search_query)
    else:
        # Handle other search types or show an error message
        flash('Invalid search type', 'error')
        return redirect(url_for('index.index'))

    # Render the search results page
    return render_template('index.html', avail_products=results,
                           page=page)




#gets products for sale for a charity 5 by default
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

#for charities to add new items to their inventory
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

        total_money_raised = Charity.calculate_total_money_raised(charityId)
        print(total_money_raised)
        graph_data = Charity.prepare_graph_data(charityId)
        print(graph_data)
        return render_template('seller_inventory.html', 
        avail_products = items,
        mynum= charityId,
        charityName = name,
        graph_data = graph_data,
    total_money = total_money_raised
        )
    else:
        return redirect(url_for('index.index'))


    # return render_template('seller_inventory.html', 
    # avail_products = items,
    # mynum= charityId)


#renders charity info page for a given charity
@bp.route('/infopage/', methods = ['GET', 'POST'])
def charity_info():

    charity_id = request.args.get('charity_id')
    print(charity_id)
    if charity_id == None:
        charity_id = current_user.getCharityId(current_user.id)
    print(charity_id)
    # 2 cases: accessing a charity info page through user side, accessing a charity info page through charity side

    #case 1: charity side
    #if current_user.is_authenticated and current_user.isCharity(current_user.id):


        # charityId = User.getCharityId(current_user.id) # TO DO: Need to make sure that this can be cast as an int
        # charityDescription = User.get_charity_description(current_user.id)
        # name = User.getCharityName(current_user.id)
        # items = SoldItem.get_charity_items(int(charityId))

        # return render_template('charity_info.html',
        #     avail_products = items,
        #     mynum= charityId,
        #     charityName = name,
        #     charityDescription = charityDescription)
    #case 2: user side:
    #else:

    print("reached after long commend thing in charity_info()")
        
    charityId = charity_id # TO DO: Need to make sure that this can be cast as an int
    charityDescription = User.getCharityDescriptionGivenCharityId(charityId)
    name = User.getCharityNameGivenCharityId(charityId)
    items = SoldItem.get_charity_items(int(charityId))

    return render_template('charity_info.html',
        avail_products = items,
        charity_id= charityId,
        charityName = name,
        charityDescription = charityDescription)

#changes charity description
@bp.route('/change_charity_description', methods = ['GET', 'POST'])
def change_charity_description():
    print("reached change_charity_description() method in index.py")


    if current_user.isCharity(current_user.id): #and current_user.getCharityId(current_user.id) == charity_id:
        charity_id = current_user.getCharityId(current_user.id)

        new_description = request.form.get('newDescription')
        print(new_description)

        # Validate new_description if necessary

        # Update the charity's description
        User.update_charity_description(charity_id, new_description)

        #flash('Charity description updated successfully.', 'success')
        return redirect(url_for('index.charity_info', charity_id=charity_id))

    flash('You do not have permission to change this charity\'s description.', 'error')
    return redirect(url_for('users.account'))



#shows items that have been sold
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


#removes items from seller list
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
    buynow = request.form.get('buynow', default=0.0, type=float)
    category = request.form.get('category', default='', type=str)
    description = request.form.get('description', default='No description available', type=str)
    image = request.form.get('image', default='', type=str)

    # Retrieve expiration date and time
    expiration_date = request.form.get('expiration_date', default='', type=str)
    expiration_time = request.form.get('expiration_time', default='', type=str)

    # Validate the form data
    if not name or not price or not expiration_date or not expiration_time:
        flash('Name, price, and expiration details are required fields.', 'error')
        return redirect(url_for('index.seller_inventory'))

    # Combine expiration date and time into a datetime object
    try:
        expiration_dt = datetime.datetime.strptime(f'{expiration_date} {expiration_time}', '%Y-%m-%d %H:%M')
    except ValueError:
        flash('Invalid expiration date or time format.', 'error')
        return redirect(url_for('index.seller_inventory'))

    charityId = User.getCharityId(current_user.id) # Ensure this returns an integer or handle exceptions

    # Add the charity item to the database
    SoldItem.add_charity_item(charityId, name, price, buynow, category, expiration_dt, image, description)

    return redirect(url_for('index.seller_inventory'))

@bp.route('/support')
def support():
    return render_template('support.html')

@bp.route('/submit_support_request', methods=['POST'])
def submit_support_request():
    # name = request.form['name']
    # email = request.form['email']
    # message = request.form['message']

    # msg = Message("Support Request from " + name,
    #               sender=email,
    #               recipients=["damiawofisayo@gmail.com"])
    # msg.body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

    # with current_app.app_context():
    #     mail.send(msg)

    return redirect(url_for('index.support'))  # adjust the redirect as needed



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
