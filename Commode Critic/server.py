from flask_app import app
from flask_app.controllers import users, reviews, commodes

DATABASE = "restroom_schema"

if __name__=="__main__":   
    app.run(debug=True)    