from flask import current_app as app
from flask import jsonify
import datetime
from humanize import naturaltime
from .bid import Bid

class Product:
    def __init__(self, id, name, price, available, catergory, expiration, image, rating):
        self.id = id
        self.name = name
        self.price = Bid.get_max_bid(id).amount if Bid.get_max_bid(id) else price#Price is instantiated as current bid amount
        self.available = available
        self.image = image
        self.catergory = catergory
        #self.expiration = expiration
        self.expiration = naturaltime(datetime.datetime.now() - expiration)
        #print("successfully set self.expiration.\n")
        self.rating = rating

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available, catergory, expiration, image, rating
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available, catergory, expiration, image, rating
FROM Products
WHERE available = :available
                              AND expiration >= now()
''',
                              available=available)
        return [Product(*row) for row in rows]
    

    @staticmethod
    def get_all_by_category(catergory, available):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE catergory = :catergory
                              AND available = :available

''',
                              available=available, catergory =catergory)
        return [Product(*row) for row in rows]
    
    

    @staticmethod
    def getPrice(id):
        rows = app.db.execute('''
SELECT price
FROM Products
WHERE id = :id
''',
                              id=id)
        return int(*(rows[0])) if rows else None

    @staticmethod
    def get_seller(id):
        row = app.db.execute('''
        SELECT charityId
        FROM Sells
        WHERE productId = :id
    ''', id=id).fetchone()
        return Product(*(row)) if row is not None else None

    def get_most_expensive():
        rows = app.db.execute('''
SELECT * FROM Products
                              WHERE expiration >= now()
ORDER BY price DESC
                              
    ''',
    available = available)
        return [Product(*row) for row in rows]
    
    
    def get_least_expensive():
        rows = app.db.execute('''
SELECT * FROM Products
                              WHERE expiration >= now()
ORDER BY price
    ''')
        return [Product(*row) for row in rows]
    
    def get_highest_rating():
        rows = app.db.execute('''
SELECT * FROM Products
                              WHERE expiration >= now()
ORDER BY rating DESC
    ''')
        return [Product(*row) for row in rows]
    
    def get_expiration():
        rows = app.db.execute('''
SELECT * FROM Products
    WHERE expiration >= now()
ORDER BY expiration;
    ''')
        return [Product(*row) for row in rows]
    

    @staticmethod
    def change_price(id, amount):
            print('MY ID:' + str(id))
            print('MY AMOUNT:' + str(amount))
            rows = app.db.execute('''
                    UPDATE Products
SET price = :amount
WHERE id = :id; ''', id=id,
amount=amount
                                )
            return id
