from flask import Flask
from os import path
from flask_login import LoginManager
from .views import views
from .auth import auth
from .models import db, User, Question, Choice

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    init_question_data()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        new_user = User(username="ren", password="renren")
        db.session.add(new_user)
        db.session.commit()

        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def init_question_data():
    question1 = Question(
        question="What programming language is commonly used for artificial intelligence development?")
    print(question1.id)
    choice_question_1 = Choice(choice="Python", question_id=question1.id)

def seed_database():
    users_data = [
        {'username': 'user1'},
        {'username': 'user2'},
        {'username': 'user3'},
    ]
    for user_info in users_data:
        existing_user = User.query.filter_by(username=user_info['username']).first()
        if not existing_user:
            user = User(**user_info)
            db.session.add(user)
    db.session.commit()

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print("ASdSDASDASDASDASDASDASD")
#         questions, choices, question_correct_choice = init_question_data()
#         # db.session.add()
#         print('Created Database!')
