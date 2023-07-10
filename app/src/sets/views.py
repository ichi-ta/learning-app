from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app import app
#from app.models import QuestionSet

sets = Blueprint("sets",__name__)

@sets.route("/sets", methods=["GET"])
def sets_get():
  sets = QuestionSet.query.all(current_user)
  return render_template("sets/sets_get.html",sets=sets)