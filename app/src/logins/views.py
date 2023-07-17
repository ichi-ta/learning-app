from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from app import app
from app.models import User

logins = Blueprint("logins", __name__)
login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@logins.route("/")
def jump_login():
  return redirect(url_for('logins.login_get'))

@logins.route("/top",methods=["GET"])
@login_required
def top_get():
  user = User.query.filter(User.id == current_user.id).first()
  return render_template("top.html",user=user)

@logins.route('/login', methods=['GET'])
def login_get():
  if current_user.is_authenticated:
    return redirect(url_for('logins.top_get'))
  return render_template('login.html')

@logins.route('/login', methods=['POST'])
def login_post():
    user = User.query.filter(User.mail==request.form["mail"]).one_or_none()
    if user is None or not user.check_password(request.form["password"]):
        flash('メールアドレスかパスワードが間違っています')
        return redirect(url_for('logins.login_post'))
    login_user(user)
    return redirect(url_for('logins.top_get'))

@logins.route('/logout')
def logout():
    logout_user()
    return render_template("login.html")