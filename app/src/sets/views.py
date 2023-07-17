from flask import Blueprint, render_template, redirect, request, url_for, abort,flash
from flask_login import current_user

from app import app
from app.models import db, QuestionSet,Question

sets = Blueprint("sets",__name__)


@sets.route("/sets", methods=["GET", "POST"])
def set_list():
  if request.method == "POST":
    set = QuestionSet(name=request.form["set_name"])
    db.session.add(set)
    db.session.commit()
    return redirect(url_for('sets.set_list'))
  else: # GET
    set = QuestionSet.query.all()
    return render_template("sets/sets_list.html",sets=set)

@sets.route("/sets/<int:set_id>", methods=["GET"])
def set_detail(set_id):
  set = QuestionSet.query.get(set_id)
  if set is None:
    abort(404)
  return render_template("sets/sets_detail.html", set=set)

@sets.route("/sets/<int:set_id>/edit", methods=["GET", "POST"])
def set_edit(set_id):
  set = QuestionSet.query.get(set_id)
  if request.method == "POST":
    action = request.form.get("action", "update_set")
    if action == "update_set":
      set.name = request.form["set_name"]
      db.session.commit()
      return redirect(url_for('sets.set_edit', set_id=set_id))
    elif action == "add_question":
      question = Question(
        sentence=request.form.get("question_sentence", ""),
        choice1=request.form.get("choice1", ""),
        choice2=request.form.get("choice2", ""),
        choice3=request.form.get("choice3", ""),
        choice4=request.form.get("choice4", ""),
        correctans=request.form.get("correctans", ""),
        questionset_id=set_id)
      db.session.add(question)
      db.session.commit()
  return render_template("sets/sets_edit.html", set=set)

@sets.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
        flash('Question not found')
        return redirect(url_for('sets.set_list'))
    db.session.delete(question)
    db.session.commit()
    flash('問題を削除しました')
    return redirect(url_for('sets.set_edit', set_id=question.questionset_id))


