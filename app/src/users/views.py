from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required


from app.models import db, User, QuestionSet

users = Blueprint("users", __name__)

@users.route("/user/new", methods=['GET'])
def user_new_form():
    return render_template("users/user_new.html")

@users.route("/user/new",methods=['POST'])
def user_new():
    #教員であればroleカラムに1を格納
    if request.form["teacher"]:
        role = 1
    else:
        role = 0

    user = User(
        name=request.form["user_name"],
        role=role,
        mail=request.form["mail"]
    )
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('logins.jump_login'))

@users.route("/teachers",methods=["GET"])
@login_required
def teacher_list():
    teachers = User.query.filter(User.role==1).all()
    return render_template("users/teacher_list.html", teachers=teachers)

@users.route("/teachers/<id>",methods=["GET"])
@login_required
def teacher_detail(id):
    teacher = User.query.filter(User.role==1, User.id==id).first()
    teacher_sets = QuestionSet.query.filter(QuestionSet.user_id==teacher.id).all()
    sets_count = len(teacher_sets)
    return render_template("users/teacher_detail.html", teacher=teacher, sets=teacher_sets, sets_count=sets_count)

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

