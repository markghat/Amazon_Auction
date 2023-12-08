from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Charity(UserMixin):
    def __init__(self, id, orgId, name, email, password, description, category, region, moneyraised):
        self.id = id
        self.orgId = orgId
        self.name = name
        self.email = email
        self.password = password
        self.description = description
        self.category = category
        self.region = region
        self.moneyraised = moneyraised

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, name
FROM Charities
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Charities
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, name):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, name)
VALUES(:email, :password, :name)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  name=name)
            id = rows[0][0]
            return User.get(id) # TODO
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, name
FROM Charities
WHERE id = :id
""",
                              id=id)
        return Charity(*(rows[0])) if rows else None
    
#     @staticmethod
#     def get_products(id):
#         rows = app.db.execute("""
# SELECT *
# FROM Products
# WHERE id = :id
# """,
#                               id=id)
#         return Charity(*(rows[0])) if rows else None

    def calculate_total_money_raised(id):
        # Query your database to sum up the total donations or money raised
        rows = app.db.execute("""
SELECT moneyraised
FROM Charities
WHERE id = :id
""",
                              id=id)
        return rows[0][0] if rows else 0

    def prepare_graph_data(charity_id):
        # Execute the SQL query to get sales data grouped by date for a specific charity
        rows = app.db.execute("""
        SELECT DATE(p.time_purchased) as purchase_date, SUM(pr.price) as total_sales
        FROM Purchases p
        JOIN Products pr ON p.pid = pr.id
        JOIN Sells s ON s.productId = pr.id
        WHERE s.charityId = :charity_id
        GROUP BY DATE(p.time_purchased)
        ORDER BY DATE(p.time_purchased)
        """,
        charity_id=charity_id)

        # Extract data for graph
        print(rows)
        labels = [row[0].strftime("%Y-%m-%d") for row in rows]  # Dates as labels
        data = [row[1] for row in rows]  # Sales data

        return {"labels": labels, "data": data}
