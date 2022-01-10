from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,redirect,session,request, flash, jsonify
from flask_app import app
import re
from flask_app.models.user import User
from flask_app.models.commode import Commode
from flask_app.models.review import Review
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/new/commode')
def new_commode():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template("add_commode.html",user=User.get_by_id(data))


@app.route('/create/commode',methods=['POST'])
def create_commode():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Commode.validate_commode(request.form):
        return redirect('/new/commode')
    data = {
        "location" : request.form['location'],
        "descript" : request.form['descript'],
        "access" : request.form['access'],
        "bowls" : request.form['bowls'],
        "urinals" : request.form['urinals'],
        "gender_neutral" : request.form['gender_neutral'],
        "baby" : request.form['baby'],
        "dispenser" : request.form['dispenser'],
        "comfy": request.form['comfy'],
        "atmosphere" : request.form['atmosphere'],
        "safety" : request.form['safety'],
        "fee" : request.form['fee'],
        "lockd" : request.form['lockd'],
        "speak" : request.form['speak'],
        "auto_flush" : request.form['auto_flush'],
        "auto_sink" : request.form['auto_sink'],
        "towel": request.form['towel'],
        "sanitizer": request.form['sanitizer'],
        "air_dryer" : request.form['air_dryer'],
        "clean" : request.form['clean'],
        }
    Commode.save(data)
    return redirect('/dashboard')

@app.route('/view/commode/<int:id>')
def show_commode(id):
    if 'user_id' in session:
        data = {
            "id":id
        }
        user_data = {
            "id":session['user_id']
        }
        commode_in_db=Commode.get_by_id(data)
        session['toilet_id'] = commode_in_db.id
        return render_template("view_commode.html",commode=Commode.get_by_id(data),user=User.get_by_id(user_data), reviews=Review.get_all_reviews_by_commode(data))
    else:
        data = {
            "id":id
        }
        commode_in_db=Commode.get_by_id(data)
        session['toilet_id'] = commode_in_db.id
        return render_template("view_commode.html",commode=Commode.get_by_id(data), reviews=Review.get_all_reviews_by_commode(data))

# @app.route('/view/commode/<int:id>/safe')
# def show_commode_safe(id):
#     data = {
#         "id":id
#         }
#     return render_template("view_commode.html",commode=Commode.get_by_id(data))

@app.route('/edit/commode/<int:id>')
def edit_commode(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_commode.html",edit=Commode.get_by_id(data),user=User.get_by_id(user_data))

@app.route('/update/commode',methods=['POST'])
def update_commode():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Commode.validate_commode(request.form):
        return redirect('/new/commode')
    data = {
        "location" : request.form['location'],
        "descript" : request.form['descript'],
        "access" : request.form['access'],
        "bowls" : request.form['bowls'],
        "urinals" : request.form['urinals'],
        "gender_neutral" : request.form['gender_neutral'],
        "baby" : request.form['baby'],
        "dispenser" : request.form['dispenser'],
        "comfy": request.form['comfy'],
        "atmosphere" : request.form['atmosphere'],
        "safety" : request.form['safety'],
        "fee" : request.form['fee'],
        "lockd" : request.form['lockd'],
        "speak" : request.form['speak'],
        "auto_flush" : request.form['auto_flush'],
        "auto_sink" : request.form['auto_sink'],
        "towel": request.form['towel'],
        "air_dryer" : request.form['air_dryer'],
        "clean" : request.form['clean'],
        "id" :request.form['id']
    }
    Commode.update(data)
    return redirect('/dashboard')

@app.route('/search')
def filter_commode():
    return render_template("search.html", commodes=Commode.get_all_commodes())