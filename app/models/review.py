from flask import current_app as app
from humanize import naturaltime
import datetime


class ProductReview:
    def __init__(self, id, uid, pid, rating, date_posted, feedback):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.date_posted = naturaltime(datetime.datetime.now() - date_posted)
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
                                ORDER BY rating DESC
                                ''',uid=uid)
        return [ProductReview(*row) for row in rows]
    
    #gets all reviews for a given product
    @staticmethod
    def get_by_pid(pid):
        rows = app.db.execute('''
                                SELECT id, uid, pid, rating, date_posted, feedback
                                FROM Reviews
                                WHERE pid = :pid
                                ORDER BY rating DESC
                                ''',pid=pid)
        return [ProductReview(*row) for row in rows]
    
    #get total number of reviews for a given product
    @staticmethod
    def get_total_number_by_id(pid):
        rows = app.db.execute('''
                                SELECT id, uid, pid, rating, date_posted, feedback
                                FROM Reviews
                                WHERE pid = :pid
                                ORDER BY rating DESC
                                ''',pid=pid)
        return [] if len(rows) == 0 else len(rows)
    
    #get average rating for a given product
    @staticmethod
    def get_average_rating(pid):
        rows = app.db.execute('''
                                SELECT CAST(AVG(rating) AS INTEGER) AS average_rating
                                FROM Reviews
                                WHERE pid = :pid
                                ''',pid=pid)
        return rows[0][0] if rows else None


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
    
    @staticmethod
    def add_review(uid, pid, rating, date_posted, feedback):
        rows = app.db.execute('''
                INSERT INTO Reviews(uid, pid, rating, date_posted, feedback)
                VALUES(:uid, :pid, :rating, :date_posted, :feedback)
                ON CONFLICT (uid, pid) DO UPDATE 
                SET rating = :rating,
                    date_posted = :date_posted,
                    feedback = :feedback
                RETURNING id; ''', uid=uid,
                              pid=pid,
                              rating=rating,
                              date_posted=date_posted,
                              feedback=feedback)
        id = rows[0][0]
        return id
    
    @staticmethod
    def get_last_review(pid, uid):
        rows = app.db.execute('''
                SELECT id, uid, pid, rating, date_posted, feedback
                FROM Reviews
                WHERE pid = :pid AND uid = :uid
            ''', pid=pid, uid=uid)
        return None if rows is None or len(rows) == 0 else ProductReview(*(rows[0]))
