from flask import current_app as app

class Cart:
    def __init__(self, cart_item_id, user_id, quantity, status):
        self.cart_item_id = cart_item_id
        self.user_id = user_id
        self.quantity = quantity
        self.status = status

    @staticmethod
    def get(cart_item_id):
        rows = app.db.execute('''
SELECT cart_item_id, user_id, quantity, status
FROM Cart
WHERE cart_item_id = :cart_item_id
''',
                              cart_item_id=cart_item_id)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_user_id(user_id):
        rows = app.db.execute('''
SELECT cart_item_id, user_id, quantity, status
FROM Cart
WHERE user_id = :user_id
ORDER BY cart_item_id DESC
''',
                              user_id=user_id)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_all_by_status(status):
        rows = app.db.execute('''
SELECT cart_item_id, user_id, quantity, status
FROM Cart
WHERE status = :status
ORDER BY cart_item_id DESC
''',
                              status=status)
        return [Cart(*row) for row in rows]
