from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from app.models import db, User

users = Blueprint("users", __name__)

@users.route("/user/new", methods=['GET'])
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
    return redirect(url_for('logins.jump_login'))

#ユーザを確認するための処理（管理者のみ）
'''
@users.route("/all_users", methods=["GET"])
def all_user_get():
    users = User.query.all()
    return render_template("users/all_user.html", users=users)

@users.route("/user/<id>/delete",methods=["POST"])
def user_delete(id):
    user = User.query.filter(User.id==id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.all_user_get'))
'''

