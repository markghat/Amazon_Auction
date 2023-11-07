from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance
        

    @staticmethod
    def get_by_auth(email, password):
        print(email)
        print(password)
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, balance
FROM Users
WHERE email = :email
""",
                              email=email)
        print(rows)
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
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, balance)
VALUES(:email, :password, :firstname, :lastname, 0)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None
    @staticmethod
    def update(id, email, password, firstname, lastname, balance):
            rows = app.db.execute("""
UPDATE Users 
SET email = :email, password = :password, firstname = :firstname, lastname = :lastname, balance = :balance
WHERE id = :id      
""",
                                  id=id,
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, balance = balance)
            return None

    # BELOW IS NEW CODE; If new user wants to register as charity
    @staticmethod
    def register_as_charity(email, password, firstname, lastname, charity_name):
        try:
            rows = app.db.execute("""
                INSERT INTO Users(email, password, firstname, lastname)
                VALUES(:email, :password, :firstname, :lastname)
                RETURNING id
                """,
                email=email,
                password=generate_password_hash(password),
                firstname=firstname, lastname=lastname)
            
            user_id = rows[0][0]

            print(type(user_id))
            print(user_id)

            print("before charities insert")
            # Insert into Charities table
            app.db.execute("""
                INSERT INTO Charities (userid, name, email, password)
                VALUES(:user_id, :charity_name, :email, :password)
                """,
                user_id=user_id,
                charity_name=charity_name,
                email=email,
                password=generate_password_hash(password))

            print("after charity insert")
            print(User.get(user_id))
            return User.get(user_id)
        except Exception as e:
            print(str(e))
            return None


    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, balance
FROM Users
WHERE id = :id
""",
                              id=id)


        return User(*(rows[0])) if rows else None
    @staticmethod
    def get_balance(id):
        rows = app.db.execute("""
        SELECT balance
FROM Users
WHERE id = :id                    
""",
                    id=id)
        print(rows[0])
        return int(*(rows[0])) if rows else None
        
    @staticmethod
    def update_balance(id, amount):
        rows = app.db.execute("""
UPDATE Users
SET balance = :amount
WHERE id = :id                        
""",
                    id=id, amount=amount)
        return None
        

    @staticmethod
    def isCharity(uid):
        try:
            rows = app.db.execute("""
SELECT userId
FROM Charities
WHERE userId = :uid
""",
                                  uid=uid)

        #return User(*(rows[0])) if rows else None
            #return True if rows else None
            return len(rows) > 0
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def getCharityId(uid):
        try:

           
            rows = app.db.execute("""
            SELECT id
            FROM Charities
            WHERE userId = :uid
            """,
                                  uid=uid)
            print("printing the ID")
            print(rows[0][0])
          

            return rows[0][0] if rows else None

            #return _ if rows else None  

            #return User(*(rows[0])) if rows else None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    def getCharityName(uid):
        try:

            print("before query")
            rows = app.db.execute("""
            SELECT name
            FROM Charities
            WHERE userId = :uid
            """,
                                  uid=uid)
            print("printing the ID")
            print(rows[0][0])
          

            return rows[0][0] if rows else None

            #return _ if rows else None  

            #return User(*(rows[0])) if rows else None
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None





