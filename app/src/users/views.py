from flask import Blueprint, render_template, request, redirect, url_for

from app.models import db, User

users = Blueprint("users", __name__)

@users.route("/user/new",methods=['GET'])
def user_new_form():
    return render_template("users/user_new.html")

@users.route("/user/new",methods=['POST'])
def user_new():
    #mailカラムの追加
    user = User(
        name=request.form["user_name"],
        mail=request.form["mail"]
    )
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('top_get')) 