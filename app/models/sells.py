from flask import current_app as app

from .product import Product


class SoldItem:
    def __init__(self, charityId):
        print("charityID is" + str(charityId))
        self.charityId = charityId
#self.productId = productId

    @staticmethod
    def get_charity_items(charityId): # get ALL items sold by a given charity (by charityId)
        rows = app.db.execute('''
SELECT P.id, P.name, P.price, P.available FROM Sells AS S JOIN Products AS P ON S.productId = P.id WHERE S.charityId = :charityId;
''',
                              charityId=charityId)
        #return [SoldItem(*rows) for rows in rows]

        ##return [SoldItem(row[0]) for row in rows]

        #for row in rows:
            #print(len(row))

        #return [row for row in rows]

        return [Product(*row) for row in rows]

"""
SELECT DISTINCT Products.name
FROM Sells, Products
WHERE Sells.charityId = :charityId AND Sells.charityid = Products.id
"""

"""
    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added
FROM Wishes
WHERE uid = :uid
AND time_added >= :since
ORDER BY time_added DESC
''',
                              uid=uid,
                              since=since)
        return [WishlistItem(*row) for row in rows]
"""
