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


    @staticmethod
    def remove_charity_item(pid):
        try:

            app.db.execute("""
                DELETE FROM Sells WHERE productId = :pid;
            """,
                                    pid = pid)

            app.db.execute("""
                DELETE FROM Products WHERE id = :pid;
            """,
                                    pid = pid)
            print("Deleted from Products:" + str(pid))



            print("Deleted from Sells:" + str(pid))
            #id = rows[0][0]
            #return Purchase.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


    @staticmethod
    def add_charity_item(charityId, price, name):
        #try:
        # Step 1: Add a new product to the Products table
        result = app.db.execute("""
            INSERT INTO Products (name, price) 
            VALUES (:name, :price)
            RETURNING id;
        """, name=name, price=price)

 

        product_id = result[0][0]
 
        #product_id = result.fetchone()[0]
        #print(product_id)
        #print(type(product_id))
        

        # Step 2: Associate the product with the charity in the Sells table
        app.db.execute("""
            INSERT INTO Sells (charityId, productId)
            VALUES (:charityId, :productId);
        """, charityId=charityId, productId=product_id)

        return 4
       # except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            #print(str(e))
            #return None
