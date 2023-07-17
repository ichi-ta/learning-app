from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session

from app import app

logins = Blueprint("logins", __name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['USERNAME'] = 'user'
app.config['PASSWORD'] = 'pass'

@logins.route('/')
def index():
    if "flag" in session and session["flag"]:
        return render_template('top.html', username=session["username"])
    return redirect('/login')

@logins.route('/login', methods=['GET'])
def login():
    if "flag" in session and session["flag"]:
        return redirect('/top')
    return render_template('login.html')

@logins.route('/login', methods=['POST'])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if username != app.config['USERNAME']:
        flash('ユーザ名が異なります')
    elif password != app.config['PASSWORD']:
        flash('パスワードが異なります')
    else:
        session["flag"] = True
        session["username"] = username
    if session["flag"]:
        return render_template('top.html', username=session["username"])
    else:
        return redirect('/login')

@logins.route('/top')
def top():
    if "flag" in session and session["flag"]:
        return render_template('top.html', username=session["username"])
    return render_template('top.html')


@logins.route('/contents')
def contents():
    if "flag" in session and session["flag"]:
        return render_template('contents.html', username=session["username"])
    return redirect('/login')

@logins.route('/logout')
def logout():
    session.pop('username', None)
    session.pop("flag", None)
    session["username"] = None
    session["flag"] = False
    flash('ログアウトしました')
    return redirect("/login")


if __name__ == '__main__':
  app.run(debug=True)