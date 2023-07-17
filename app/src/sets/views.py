from flask import Blueprint, Response, render_template, redirect, request, url_for
from flask_login import current_user

from app import app
from app.models import db, QuestionSet

sets = Blueprint("sets",__name__)

@sets.route("/sets", methods=["GET"])
def sets_get():
  sets = QuestionSet.query.filter(QuestionSet.user_id == current_user.id).all()
  return render_template("sets/sets_get.html",sets=sets)

#学習セット作成フォームの処理
@sets.route("/sets", methods=["POST"])
def sets_post():
  set = QuestionSet(
    name=request.form["set_name"],
    user_id=current_user.id
  )
  db.session.add(set)
  db.session.commit()
  return redirect(url_for('sets.sets_get'))

#学習セット詳細ページの処理
@sets.route("/sets/<set_id>",methods=["GET"])
def sets_detail(set_id):
  set = QuestionSet.query.filter(QuestionSet.user_id==current_user.id, QuestionSet.id==set_id).first()
  return render_template("sets/set_detail.html", set=set)