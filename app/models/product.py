from flask import current_app as app
from flask import jsonify


class Product:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available, catergory, expiration, image
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available, catergory, expiration, image
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    def get_most_expensive(k):
        rows = app.db.execute('''
SELECT * FROM Products
ORDER BY price DESC
    ''')
        return [Product(*row) for row in rows[:k]]
