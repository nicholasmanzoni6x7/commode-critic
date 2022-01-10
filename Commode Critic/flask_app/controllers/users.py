from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,redirect,session,request, flash
from flask_app import app
import re
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.models.commode import Commode
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html', commodes=Commode.get_all_commodes())

@app.route('/getstarted')
def get_started():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['pw'])
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "user_name": request.form['user_name'],
        "pw": pw_hash
    }
    print(data)
    user_id = User.save(data)
    user_name = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = user_name
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    data = { "email" : request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("Invalid Email","log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.pw, request.form['pw']):
        flash("Invalid Password","log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.user_name
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({'id' :session['user_id']})
    reviews = Review.get_all_by_user({'user_id':session['user_id']})
    return render_template("dashboard.html", user = user, reviews=reviews)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')