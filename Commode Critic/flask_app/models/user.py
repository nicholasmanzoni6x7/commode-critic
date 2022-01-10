from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.review import Review

class User:
    DATABASE = "restroom_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.user_name = data['user_name']
        self.pw = data['pw']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reviews=[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, user_name, pw, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(user_name)s, %(pw)s,  NOW(), NOW());"
        return connectToMySQL(cls.DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DATABASE).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all_reviews_with_user(cls, data):
        query ="SELECT * FROM users LEFT JOIN reviews ON users.id = reviews.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            review= cls(results[0])
            for row in results:
                your_reviews={
                    "id" : row["reviews.id"],
                    "content" : row["content"],
                    "comfy_rate" : row["comfy_rate"],
                    "atmos_rate" : row["atmos_rate"],
                    "safe_rate" : row["safe_rate"],
                    "clean_rate" : row["clean_rate"],
                    "created_at" : row["reviews.created_at"],
                    "updated_at" : row["reviews.updated_at"],
                }
                User.reviews.append(Review(your_reviews))
            return review
        return False

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DATABASE).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","reg")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","reg")
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters","reg")
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters","reg")
            is_valid= False
        if len(user['pw']) < 9:
            flash("Password must be at least 8 characters","reg")
            is_valid= False
        if user['pw'] != user['con_pass']:
            flash("Passwords don't match","reg")
        return is_valid