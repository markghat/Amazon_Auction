from flask import current_app as app

from .product import Product
from .order import Order
from .bid import Bid


class SoldItem:
    def __init__(self, charityId):
        print("charityID is" + str(charityId))
        self.charityId = charityId
#self.productId = productId

    @staticmethod
    def get_charity_items(charityId): # get ALL items sold by a given charity (by charityId)
        # Original query: 
        #SELECT P.id, P.name, P.price, P.available FROM Sells AS S JOIN Products AS P ON S.productId = P.id WHERE S.charityId = :charityId;
        rows = app.db.execute('''
SELECT P.id, P.name, P.price, P.available, P.catergory,P.expiration, P.image, P.rating FROM Sells AS S JOIN Products AS P ON S.productId = P.id WHERE S.charityId = :charityId AND P.available = true;
''',
                              charityId=charityId)
        #return [SoldItem(*rows) for rows in rows]

        ##return [SoldItem(row[0]) for row in rows]

        #for row in rows:
            #print(len(row))

        #return [row for row in rows]
        # print("IN get_charity_items() method in sells.py!!!!!!")
        # print("P.id=" + str(rows[0][0]))
        # print("P.name=" + str(rows[0][1]))
        # print("P.price=" + str(rows[0][2]))
        # print("P.available=" + str(rows[0][3]))
        # print("P.image=" + str(rows[0][0]))

        # print("\n\n\n")

        return [Product(*row) for row in rows]


    @staticmethod
    def get_charity_orders(charityId): # get ALL items sold by a given charity (by charityId)
        rows = app.db.execute('''
            SELECT O.id, O.purchaseId, O.productName, O.buyerId, O.sellerId, O.date_placed, O.total_cost, O.status
            FROM Orders AS O
            WHERE O.sellerId = :charityId;
        ''', charityId=charityId)

        return [Order(*row) for row in rows]


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
    def add_charity_item(charityId, name, price, category, expiration, image):
        #try:
        # Step 1: Add a new product to the Products table

        # result = app.db.execute("""
        #     INSERT INTO Products (name, price) 
        #     VALUES (:name, :price)
        #     RETURNING id;
        # """, name=name, price=price)
                # Step 1: Add a new product to the Products table
        result = app.db.execute("""
            INSERT INTO Products (name, price, available, catergory, expiration, image, rating) 
            VALUES (:name, :price, TRUE, :category, :expiration, :image, 0.0)
            RETURNING id;
        """, name=name, price=price, category=category, expiration=expiration, image=image)
        

        product_id = result[0][0]

        #expiration_test = result[0][5]
       # print("expiration:")
        #print(expiration_test)
        ##print(type(expiration_test))
 
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


    @staticmethod
    def update_available(product_id, new_status): # for example, new_status = False or new_status = True
        try:
            app.db.execute("""
                UPDATE Products
                SET available = :new_status
                WHERE id = :product_id;
            """, new_status=new_status, product_id=product_id)

            print(f"Product {product_id} availability updated to {new_status}")
        except Exception as e:
            print(f"Error updating product availability: {str(e)}")

    def search_by_seller(search_query): # TODO: CHANGE THISSSSS
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE LOWER(name) LIKE LOWER(:name)
''', name='%'+search_query+'%')
        return [Product(*row) for row in rows]
    
