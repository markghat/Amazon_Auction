from flask import current_app as app


class ProductReview:
    def __init__(self, id, uid, pid, rating, date_posted, feedback):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.date_posted = date_posted
        self.feedback = feedback

    #gets all reviews
    @staticmethod
    def get_all():
        rows = app.db.execute('''
                                SELECT id, uid, pid, rating, date_posted, feedback
                                FROM Reviews
                                ''')
        return [ProductReview(*row) for row in rows]
    
    #gets a review
    @staticmethod
    def get(id):
        rows = app.db.execute('''
                                SELECT id, uid, pid, rating, date_posted, feedback
                                FROM Reviews
                                WHERE id = :id
                                ''',id=id)
        return [ProductReview(*row) for row in rows]

    #gets all reviews by a given user
    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
                                SELECT id, uid, pid, rating, date_posted, feedback
                                FROM Reviews
                                WHERE uid = :uid
                                ''',uid=uid)
        return [ProductReview(*row) for row in rows]

    #finds 5 most recent reviews for a given user
    @staticmethod
    def get_5_most_recent(uid):
        rows = app.db.execute('''
                                SELECT id, uid, pid, rating, date_posted, feedback
                                FROM Reviews
                                WHERE uid = :uid
                                ORDER BY date_posted DESC
                                LIMIT 5
                                ''', uid=uid)
        return [ProductReview(*row) for row in rows]

    #delete reviews
    @staticmethod
    def delete_by_id(id):
        rows = app.db.execute('''
                            DELETE FROM Reviews
                            WHERE id = :id; ''',id=id)
        return None
