from flask import current_app as app
import datetime
from .. import login
from .product import Product

class Cart:
    def __init__(self, product_id, product_name, buyer_id, product_price, seller_id):
        self.product_id = product_id
        self.product_name = product_name
        self.buyer_id = buyer_id
        self.product_price = product_price
        self.seller_id = seller_id 
    
    #gets what's currently in a given users cart
    @staticmethod
    def get_cart_for_user(buyer_id):
        rows = app.db.execute('''
        SELECT Cart.product_id, Products.name, Cart.buyer_id, Products.price As product_price, Sells.charityId As seller_id
        FROM Cart
        JOIN Products ON Cart.product_id = Products.id
        LEFT JOIN Sells ON Products.id = Sells.productId 
        WHERE Cart.buyer_id = :buyer_id
        ''', buyer_id=buyer_id)
        return [Cart(*row) for row in rows]

    #adds a product to a users cart for a given user id and product id
    @staticmethod
    def add_to_cart(buy_id, product_id):
        print(f"Attempting to add product {product_id} to cart for user {buy_id}")
        rows = app.db.execute('''
        SELECT * FROM Cart WHERE buyer_id=:buy_id AND product_id=:product_id;
        ''', buy_id=buy_id, product_id=product_id)
        print(f"Product already in cart check returned: {rows}")
        # If not in the cart
        if len(rows) == 0:
            app.db.execute('''
            INSERT INTO Cart(product_id, buyer_id)
            VALUES (:product_id, :buy_id);
            ''', product_id=product_id, buy_id=buy_id)
            return "Product added to cart."
        # If already in the cart
        else: 
            print(f"Product {product_id} is already in the cart for user {buy_id}")
            return "Product already in the cart."

    #removes a product from a users cart for a given product and user id
    @staticmethod
    def remove_from_cart(buyer_id, product_id):
        rows = app.db.execute('''
        DELETE FROM Cart WHERE buyer_id=:buy_id AND Cart.product_id=:product_id;
        ''', buy_id=buyer_id, product_id=product_id)
        return rows
