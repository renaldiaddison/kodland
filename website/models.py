from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import composite

db = SQLAlchemy()

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    scores = db.relationship('Score')

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(150))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    choices = db.relationship('Choice')

class QuestionCorrectChoice(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct_choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))

    __table_args__ = (
        db.PrimaryKeyConstraint('question_id', 'correct_choice_id'),
    )