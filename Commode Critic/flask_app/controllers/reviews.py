from flask_app.config.mysqlconnection import connectToMySQL
from flask import render_template,redirect,session,request, flash, jsonify
from flask_app import app
import re
from flask_app.models.user import User
from flask_app.models.review import Review
from flask_app.models.commode import Commode
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

DATABASE = "restroom_schema"

@app.route('/commmode/<int:id>/review')
def new_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }

    commode_data={
        "id":id
    }
    
    return render_template("add_review.html",user=User.get_by_id(user_data), commode=Commode.get_by_id(commode_data))


@app.route('/create/review',methods=['POST'])
def create_review():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Review.validate_review(request.form):
        return redirect('/new/review')
    data = {
        "user_id": session["user_id"],
        "toilet_id":session["toilet_id"],
        "location":request.form["location"],
        "content": request.form["content"],
        "comfy_rate": int(request.form["comfy_rate"]),
        "atmos_rate": int(request.form["atmos_rate"]),
        "safe_rate": int(request.form["safe_rate"]),
        "clean_rate": int(request.form["clean_rate"]),
        "created_by": session["user_name"]
    }
    Review.save(data)
    return redirect('/dashboard')

@app.route('/edit/review/<int:id>')
def edit_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("edit_review.html",edit=Review.get_one_by_id(data),user=User.get_by_id(user_data))

@app.route('/update/review',methods=['POST'])
def update_review():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Review.validate_review(request.form):
        return redirect(f"/edit/review/{request.form['id']}")
    data = {
        "content": request.form["content"],
        "comfy_rate": int(request.form["comfy_rate"]),
        "atmos_rate": int(request.form["atmos_rate"]),
        "safe_rate": int(request.form["safe_rate"]),
        "clean_rate": int(request.form["clean_rate"]),
        "id": request.form['id']    
    }
    Review.update(data)
    return redirect('/dashboard')



@app.route('/review/<int:id>')
def show_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    
    return render_template("view_review.html",review=Review.get_one_by_id(data),user=User.get_by_id(user_data))

@app.route('/destroy/review/<int:id>')
def delete_review(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Review.destroy(data)
    return redirect('/dashboard')