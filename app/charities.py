from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from .models.product import Product
from .models.charity import Charity
from .models.sells import SoldItem
from .models.user import User

from flask import Blueprint
bp = Blueprint('charities', __name__)

@bp.route('/charity/dashboard')
def charity_dashboard(charity_id):
    listings = SoldItem.get_charity_items(charity_id) 
    charity_info = Charity.get_charity_info(charity_id)

    total_money_raised = Charity.calculate_total_money_raised(charity_id)
    graph_data = Charity.prepare_graph_data(charity_id)
    return render_template('seller_products.html', 
    graphData = graph_data,
    total_money_raised = total_money_raised,                
    avail_products = listings,
    mynum= charity_id)

@bp.route('/charity/edit', methods=['GET', 'POST'])
def edit_charity_info():
    # Handle form submission for editing charity info
    if request.method == 'POST':
        # Process form data and update charity info
        pass
    # Rest of the route implementation
    return render_template('edit_charity_info.html')

@bp.route('/charity/upload', methods=['GET', 'POST'])
def seller_inventory():
    #charityId = request.args.get('charityId', default=5, type=int)
    #print("in function")
    
    #items = SoldItem.get_charity_items(int(charityId))

    #if current_user.is_authenticated: #and User.isCharity(current_user.id):
    if current_user.is_authenticated and User.isCharity(current_user.id):
        # WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
        # return redirect(url_for('wishlist.wishlist'))

        charityId = User.getCharityId(current_user.id) # TO DO: Need to make sure that this can be cast as an int


        name = User.getCharityName(current_user.id)
        
        items = SoldItem.get_charity_items(int(charityId))

        return render_template('seller_inventory.html', 
        avail_products = items,
        mynum= charityId,
        charityName = name)
    else:
        return redirect(url_for('index.index'))