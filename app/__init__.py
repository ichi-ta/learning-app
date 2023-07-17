from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required

app = Flask(__name__)

from app.src.logins.views import logins
from app.src.users.views import users

app.register_blueprint(logins)
app.register_blueprint(users)