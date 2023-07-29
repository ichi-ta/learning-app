from flask import Blueprint, render_template, redirect, request, url_for, abort,flash,jsonify
from flask_login import current_user
from sqlalchemy.sql import text

from app import app
from app.models import db, User, QuestionSet,Question,UserAnswer

sets = Blueprint("sets",__name__)


@sets.route("/sets", methods=["GET", "POST"])
def set_list():
  if request.method == "POST":
    set = QuestionSet(name=request.form["set_name"], user_id=current_user.id)
    db.session.add(set)
    db.session.commit()
    return redirect(url_for('sets.set_list'))
  else: # GET
    student_sets = QuestionSet.query.filter(QuestionSet.user_id == current_user.id).all()
    teachers = User.query.filter_by(role=1).all()
    teacher_sets = {}
    for teacher in teachers:
        question_sets = teacher.question_sets
        teacher_sets[teacher] = question_sets
    return render_template("sets/sets_list.html", t=teachers, s_sets=student_sets)

@sets.route("/sets/<int:set_id>", methods=["GET"])
def set_detail(set_id):
    set = QuestionSet.query.get(set_id)
    if set is None:
        abort(404)

    answers = [question.correctans for question in set.questions]
    return render_template("sets/sets_detail.html", set=set, answers=answers)

@sets.route("/sets/<int:set_id>/edit", methods=["GET", "POST"])
def set_edit(set_id):
  set = QuestionSet.query.get(set_id)
  if set.user_id != current_user.id:
     flash("他人のセットは編集できません")
     return redirect(url_for('sets.set_detail', set_id=set_id))
  else:
    if request.method == "POST":
      action = request.form.get("action", "update_set")
      if action == "update_set":
        set.name = request.form["set_name"]
        db.session.commit()
        return redirect(url_for('sets.set_edit', set_id=set_id))
      #問題の追加
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

@sets.route('/sets/<int:set_id>/delete', methods=['POST'])
def delete_set(set_id):
    set = QuestionSet.query.get(set_id)
    if set.user_id != current_user.id:
       flash('他人のセットは削除できません')
       return redirect(url_for('sets.set_list'))
    else:
      if set is None:
          flash('Set not found')
          return redirect(url_for('sets.set_list'))
      db.session.delete(set)
      db.session.commit()
      flash('セットを削除しました')
      return redirect(url_for('sets.set_list'))

#問題セットの学習開始
@sets.route("/sets/<int:set_id>/start", methods=["GET"])
def set_start(set_id):
  set = QuestionSet.query.get(set_id)
  set.learn_count = 0
  if set is None:
    abort(404)
  set.learn_count += 1
  db.session.commit()
  
  questions = Question.query.filter_by(questionset_id=set.id).all()

  # Convert each question to a dict that can be serialized to JSON
  questions_json = []
  for question in questions:
    question_dict = {
      'id': question.id,
      'sentence': question.sentence,
      'choice1': question.choice1,
      'choice2': question.choice2,
      'choice3': question.choice3,
      'choice4': question.choice4,
      'correctans': question.correctans,
      'questionset_id': question.questionset_id
    }
    questions_json.append(question_dict)
  
  return render_template("sets/sets_start.html", set=set,questions=questions_json)

@sets.route('/sets/submit_answer', methods=['POST'])
def submit_answer():
    selected_answer = request.form.get('chosenAnswer')
    question_id = request.form.get('questionId')
    questionset_id = request.form.get('questionSetId')
    user_id = current_user.get_id()

    answer = UserAnswer(user_id=user_id, questionset_id=questionset_id, question_id=question_id, selected_answer=selected_answer)
    db.session.add(answer)
    db.session.commit()

    return jsonify({'success': True})