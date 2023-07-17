from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user

from app.models import User

logins = Blueprint("logins", __name__)

@logins.route('/login', methods=['POST'])
def login_post():
    user = User.query.filter_by(mail=request.form["mail"]).one_or_none()
    if user is None or not user.check_password(request.form["password"]):
        flash('メールアドレスかパスワードが間違っています')
        return redirect(url_for('logins.login_post'))
    login_user(user)
    return redirect(url_for('top_get'))

@logins.route('/logout')
def logout():
    logout_user()
    return redirect("/login")