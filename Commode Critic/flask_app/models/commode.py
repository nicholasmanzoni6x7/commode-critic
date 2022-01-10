from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.review import Review

class Commode:
    DATABASE = "restroom_schema"
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.descript = data['descript']
        self.access = data['access']
        self.bowls = data['bowls']
        self.urinals = data['urinals']
        self.gender_neutral = data['gender_neutral']
        self.baby = data['baby']
        self.dispenser = data['dispenser']
        self.comfy= data['comfy']
        self.atmosphere = data['atmosphere']
        self.safety = data['safety']
        self.fee = data['fee']
        self.lockd = data['lockd']
        self.speak = data['speak']
        self.auto_flush = data['auto_flush']
        self.auto_sink = data['auto_sink']
        self.air_dryer = data['air_dryer']
        self.sanitizer = data['sanitizer']
        self.clean = data['clean']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reviews=[]

    @classmethod
    def save(cls,data):
        query = "INSERT INTO toilets (location, descript, access, bowls, urinals, gender_neutral, baby, dispenser, comfy, atmosphere, safety, fee, lockd, speak, auto_flush, auto_sink, towel, air_dryer, sanitizer, clean, created_at, updated_at) VALUES (%(location)s, %(descript)s, %(access)s, %(bowls)s, %(urinals)s, %(gender_neutral)s, %(baby)s, %(dispenser)s, %(comfy)s, %(atmosphere)s, %(safety)s, %(fee)s, %(lockd)s, %(speak)s, %(auto_flush)s, %(auto_sink)s, %(towel)s, %(air_dryer)s, %(sanitizer)s, %(clean)s, NOW(), NOW());"
        return connectToMySQL(cls.DATABASE).query_db(query,data)

    @classmethod
    def get_all_commodes(cls):
        query = "SELECT * FROM toilets;"
        results = connectToMySQL(cls.DATABASE).query_db(query)
        all_commodes = []
        for row in results:
            all_commodes.append( cls(row))
        return all_commodes

    @classmethod
    def get_one_by_location(cls,data):
        query = "SELECT * FROM toilets WHERE location = %(location)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM toilets WHERE id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        commodes = cls(results[0])
        return commodes

    # @classmethod
    # def get_commode_with_reviews(cls , data):
    #     query = "SELECT * FROM toilets LEFT JOIN reviews ON reviews.toilet_id = toilets.id WHERE toilets.id = %(id)s;"
    #     results = connectToMySQL(cls.DATABASE).query_db(query, data)
    #     if results:# results will be a list of objects with the data attached to each row. 
    #         commode_reviews = cls( results[0] )
    #         for row in results:
    #     # Now we parse the  data to make instances of reviews and add them into our list.
    #             review_data = {
    #                 "id" : row["reviews.id"],
    #                 "user_id": row["user_id"],
    #                 "toilet_id": row["toilet_id"],
    #                 "content" : row["content"],
    #                 "comfy_rate" : row["comfy_rate"],
    #                 "atmos_rate" : row["atmos_rate"],
    #                 "safe_rate" : row["safe_rate"],
    #                 "clean_rate" : row["clean_rate"],
    #                 "created_at" : row["reviews.created_at"],
    #                 "updated_at" : row["reviews.updated_at"],
    #             }
    #         commode_reviews.reviews.append(Review(review_data))
    #         return commode_reviews
    #     return False
    


    @staticmethod
    def validate_commode(commode):
        is_valid = True
        query = "SELECT * FROM toilets WHERE location = %(location)s;"
        results = connectToMySQL(Commode.DATABASE).query_db(query,commode)
        if len(results) >= 5:
            flash("Too many commodes exist at location. Review an existing commode or contact support.","commode")
            is_valid=False
        if len(commode['location']) < 5:
            flash("Please enter a valid location","commode")
            is_valid= False
        if len(commode['descript']) < 3:
            flash("Please provide a description of the restroom","commode")
            is_valid= False
        return is_valid