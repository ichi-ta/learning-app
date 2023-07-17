from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required

app = Flask(__name__)

@app.route("/top",methods=["GET"])
@login_required
def top_get():
  return render_template("top.html")

from app.src.logins.views import logins
from app.src.users.views import users
from app.src.sets.views import sets

app.register_blueprint(logins)
app.register_blueprint(users)
app.register_blueprint(sets)