from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Review:
    DATABASE = 'restroom_schema'
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.comfy_rate = data['comfy_rate']
        self.atmos_rate = data['atmos_rate']
        self.safe_rate = data['safe_rate']
        self.clean_rate = data['clean_rate']
        self.created_by = data['created_by']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO reviews (user_id, toilet_id, content, comfy_rate, atmos_rate, safe_rate, clean_rate, created_by, created_at, updated_at) VALUES (%(user_id)s, %(toilet_id)s, %(content)s, %(comfy_rate)s, %(atmos_rate)s, %(safe_rate)s, %(clean_rate)s, %(created_by)s, NOW(), NOW());"
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM reviews;"
        results =  connectToMySQL(cls.DATABASE).query_db(query)
        all_reviews = []
        for row in results:
            all_reviews.append( cls(row) )
        return all_reviews
    
    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM reviews WHERE id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            return cls( results[0] )
    @classmethod
    def get_one_by_location(cls,data):
        query = "SELECT * FROM reviews WHERE location = %(location)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            return cls( results[0] )

    @classmethod
    def get_all_reviews_by_commode(cls,data):
        query = "SELECT * FROM reviews WHERE toilet_id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            all_reviews_by_commode=[]
            for row in results:
                all_reviews_by_commode.append(cls(row))
            return all_reviews_by_commode

    @classmethod
    def get_all_by_location(cls,data):
        query = "SELECT * FROM toilets WHERE location = %(location)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            all_by_local=[]
            for row in results:
                all_by_local.append(cls(row))
            return all_by_local

    @classmethod
    def get_all_by_user(cls,data):
        query = "SELECT * FROM reviews WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            all_by_user=[]
            for row in results:
                all_by_user.append(cls(row))
            return all_by_user

    @classmethod
    def update(cls, data):
        query = "UPDATE reviews SET content=%(content)s, comfy_rate=%(comfy_rate)s, atmos_rate=%(atmos_rate)s, safe_rate=%(safe_rate)s, clean_rate=%(clean_rate)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.DATABASE).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM reviews WHERE id = %(id)s;"
        return connectToMySQL(cls.DATABASE).query_db(query,data)

    @staticmethod
    def validate_review(review):
        is_valid = True
        if len(review['location']) < 3:
            is_valid = False
            flash("Location is required","review")
        if len(review['content']) < 3:
            is_valid = False
            flash("You must detail your review","review")
        if int(review['clean_rate']) < 1:
            is_valid=False
            flash("Commodes must be rated on cleanliness", "review")
        if (review['created_by']) != (session['user_name']):
            is_valid=False
            flash("Reviews must be signed by their authors", "review")
        return is_valid