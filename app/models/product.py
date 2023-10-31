from flask import current_app as app
from flask import jsonify
import datetime
from humanize import naturaltime

class Product:
    def __init__(self, id, name, price, available, catergory, expiration, image, rating):
        self.id = id
        self.name = name
        self.price = price
        self.available = available
        self.image = image
        self.catergory = catergory
        self.expiration = naturaltime(datetime.datetime.now() - expiration)
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
''',
                              available=available)
        return [Product(*row) for row in rows]

    def get_most_expensive():
        rows = app.db.execute('''
SELECT * FROM Products
ORDER BY price DESC
    ''')
        return [Product(*row) for row in rows]
    
    def get_least_expensive():
        rows = app.db.execute('''
SELECT * FROM Products
ORDER BY price
    ''')
        return [Product(*row) for row in rows]
    
    def get_highest_rating():
        rows = app.db.execute('''
SELECT * FROM Products
ORDER BY rating DESC
    ''')
        return [Product(*row) for row in rows]
    
    def get_expiration():
        rows = app.db.execute('''
SELECT * FROM Products
ORDER BY expiration;
    ''')
        return [Product(*row) for row in rows]
