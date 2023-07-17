from flask import Flask, render_template, redirect, url_for
from flask_login import current_user

app = Flask(__name__)

@app.route("/", methods=["GET"])
def top_get():
  if current_user.is_authenticated:
    return render_template("top.html")
  return redirect(url_for("logins.login_post"))

from app.src.logins.views import logins
from app.src.users.views import users

app.register_blueprint(logins)
app.register_blueprint(users)