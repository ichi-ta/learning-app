from flask import Blueprint, Response, render_template, redirect, request, url_for
from flask_login import current_user

from app import app
from app.models import db, QuestionSet

sets = Blueprint("sets",__name__)

@sets.route("/<user_id>/sets", methods=["GET"])
def sets_get(user_id):
  # ログインユーザのIDを取得し、自分の個別ページのみ開けるようにする
  if str(current_user.user_id) != str(user_id):
      return Response(response="他人の学習セット一覧は開けません", status=403)
  sets = QuestionSet.query.filter(current_user.user_id == user_id).all()
  return render_template("sets/sets_get.html",sets=sets)

#学習セット作成フォームの処理
@sets.route("/<user_id>/sets", methods=["POST"])
def sets_post(user_id):
  #name：フォームからの入力, user_id：引数からの入力
  set = QuestionSet(name=request.form["set_name"], user_id=user_id)
  db.session.add(set)
  db.session.commit()
  return redirect(url_for('sets.sets_get'))

#学習セット詳細ページの処理
@sets.route("/<user_id>/sets/<set_id>",methods=["GET"])
def sets_detail(user_id, set_id):
  set = QuestionSet.query.filter(current_user.user_id == user_id).get(set_id)
  return render_template("sets/set_detail.html", set=set)