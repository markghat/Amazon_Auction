from flask import current_app as app
from flask_login import current_user


class Bid:
    def __init__(self, id, uid, pid, amount): #!!!Added Name
        self.uid = uid
        self.id = id
        self.pid = pid
        self.amount = amount
        # self.bidtime= bidtime

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT *
FROM Bids
WHERE id = :id
''',
                              id=id)
        return Bid(*(rows[0])) if rows else None
    
    @staticmethod
    def get_bids(uid): 
        rows = app.db.execute('''
SELECT Bids.id, Bids.pid, Bids.amount, Products.name
FROM Bids, Products
WHERE uid = :uid and bids.pid = Products.id

''',
                              uid=uid)
        return [Bid(*row) for row in rows]
    @staticmethod
    def get_max_bid(id):
        rows = app.db.execute('''
SELECT *
FROM Bids AS B
WHERE B.pid = :id
ORDER BY B.amount DESC
LIMIT 1;
''',
                              id=id)
        return Bid(*(rows[0])) if rows else None



    @staticmethod
    def add_bid(uid, pid, amount):
            rows = app.db.execute('''
                    INSERT INTO Bids(uid, pid, amount)
                    VALUES(:uid, :pid, :amount)
                    ''', uid=uid,
                                pid=pid,
                                amount=amount,
                                )
            rows = app.db.execute("""
UPDATE Users
SET balance = balance - (SELECT max(amount) FROM Bids WHERE pid = :pid)
WHERE id = :uid
""",
                                  uid=uid,
                                  pid=pid,
                                  )
            return uid