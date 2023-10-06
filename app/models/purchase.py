from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased): 
        #self.name = name #add a name attribute?
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
    #should I create a getName function that just joins with product?
    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def add_purchase(uid, pid, time_purchased):
        try:
            rows = app.db.execute("""
INSERT INTO PURCHASES(uid, pid, time_purchased)
VALUES(:uid, :pid, :time_purchased)
RETURNING id
""",
                                  uid=uid,
                                  pid=pid,
                                  time_purchased=time_purchased)
            id = rows[0][0]
            return Purchase.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None