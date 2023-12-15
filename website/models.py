from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

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
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(150))
    correct_choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'))
    choices = db.relationship('Choice')
    
class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(150))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))