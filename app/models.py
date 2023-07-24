from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "db"
DB_NAME = "flask_app"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    role = db.Column(db.Boolean, default=False, nullable=False)
    question_sets = db.relationship('QuestionSet', backref='user', lazy=True)
    answers = db.relationship('UserAnswer', back_populates='user', lazy=True)  

    mail = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    # パスワードをハッシュ化
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
    def check_password(self, password):
        return check_password_hash(self.password, password)

class QuestionSet(db.Model):
    __tablename__ = 'questionset'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    learn_count = db.Column(db.Integer, default=0)
    good_count = db.Column(db.Integer, default=0)

    questions = db.relationship("Question", back_populates="questionset")
    answers = db.relationship('UserAnswer', back_populates='questionset', lazy=True)  

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(128))
    choice1 = db.Column(db.String(128))
    choice2 = db.Column(db.String(128))
    choice3 = db.Column(db.String(128))
    choice4 = db.Column(db.String(128))
    correctans = db.Column(db.String(128))
    questionset_id = db.Column(db.Integer, db.ForeignKey('questionset.id'))

    questionset = db.relationship("QuestionSet", back_populates="questions")
    answers = db.relationship('UserAnswer', back_populates='question', lazy=True)  

class UserAnswer(db.Model):
    __tablename__ = 'useranswer'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    questionset_id = db.Column(db.Integer, db.ForeignKey('questionset.id'))  
    selected_answer = db.Column(db.String(128))

    user = db.relationship("User", back_populates="answers")
    question = db.relationship("Question", back_populates="answers")
    questionset = db.relationship("QuestionSet", back_populates="answers") 