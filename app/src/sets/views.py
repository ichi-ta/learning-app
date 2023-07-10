from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user

from app import app
from app.models import QuestionSet

sets = Blueprint("sets",__name__)

@sets.route("/sets", methods=["GET"])
def sets_get():
  set = QuestionSet.query.all(current_user)
  return render_template("sets/sets_get.html",sets=set)

@sets.route("/sets", methods=["POST"])
def sets_post():
  set = QuestionSet(name=request.form["set_name"])
  return render_template("sets/sets_post")
  