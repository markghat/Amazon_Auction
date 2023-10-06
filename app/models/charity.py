from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Charity(UserMixin):
    def __init__(self, id, orgId, name, email, password):
        self.id = id
        self.orgId = orgId
        self.name = name
        self.email = email
        self.password = password

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
