from flask import current_app as app
from flask_login import current_user
from .user import User


class Purchase:
    def __init__(self, purchaseId, uid, pid, time_purchased, name, price): #!!!Added Name
        self.id = purchaseId
        self.name = name #!!!Added
        self.price = price #!!!Added
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    #returns the product purchased by id
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT Purchases.id, uid, pid, time_purchased, Products.name, Products.price
            FROM Purchases
            JOIN Products ON Purchases.pid = Products.id
            WHERE Purchases.id = :id
        ''', id=id)
        return Purchase(*rows[0]) if rows else None
    #returns all purchased products since given date
    @staticmethod
    def get_all_by_uid_since(uid, since): 
        rows = app.db.execute('''
SELECT Purchases.id, uid, pid, time_purchased, Products.name, Products.price
FROM Purchases, Products
WHERE uid = :uid and Purchases.pid = Products.id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    # Marks product as purchased (inserts into Purchases table); updates buying User and Charity balances
    @staticmethod
    def add_purchase(uid, pid, time_purchased, price): 
        rows = app.db.execute("""
INSERT INTO PURCHASES(uid, pid, time_purchased)
VALUES(:uid, :pid, :time_purchased)
RETURNING id
""",
                                uid=uid,
                                pid=pid,
                                time_purchased=time_purchased)
        
        rows4 = app.db.execute("""
UPDATE Products
SET price = :price
WHERE Products.id = :pid
""",
                                uid=uid,
                                pid=pid,
                                price=price
                                )

        # decrement buyer's balance
        rows2 = app.db.execute("""
UPDATE Users
SET balance = balance - :price
WHERE Users.id = :uid
""",
                                uid=uid,
                                pid=pid,
                                price=price
                                )
        cid = User.getCharityIdWithProductId(pid)
        charity_uid = User.getUserIdByCharityId(cid)

        #increment Charity's balance

        rows3 = app.db.execute("""
UPDATE Users
SET balance = balance + :price
WHERE Users.id = :uid
""",
                                uid=charity_uid,
                                pid=pid,
                                price=price
                                )
        
        rows5 = app.db.execute("""
UPDATE Charities
SET moneyraised = moneyraised + :price
WHERE Charities.id = :id
""",
                                id=cid,
                                pid=pid,
                                price=price
                                )
        

        print("value of id")
        print(cid)
        print(rows[0][0])
        #print(id)
        print("type of id:")
        #print(type(id))
        print("\n")

        return Purchase.get(rows[0][0])
        #except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            #print(str(e))
            #return None