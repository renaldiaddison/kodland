from flask import Flask
from os import path
from flask_login import LoginManager
from .views import views
from .auth import auth
from .models import db, User, Question, Choice, QuestionCorrectChoice

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ASDASDASJDKLJASD ASDKJASLKDJLKSA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        db.create_all()
        seed_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def seed_database():
    user_data = {'username': 'ren', 'password': 'asd123'}

    questions_data = [
        {'question': 'What programming language is commonly used for artificial intelligence development?'},
        {'question': 'How does Python contribute to artificial intelligence development?'},
        {'question': 'Are there specific libraries in Python commonly used for AI development?'},
        {'question': 'How can users measure and improve the performance of an AI model after implementing it into a Python application?'},
        {'question': 'What is the main role of Python in developing NLP applications?'}
    ]

    choices_data = [
        {'choice': 'Python', 'question_id': 1},
        {'choice': 'Java', 'question_id': 1},
        {'choice': 'C++', 'question_id': 1},
        {'choice': 'Ruby', 'question_id': 1},
        {'choice': 'Python provides a variety of libraries and frameworks for AI development.', 'question_id': 2},
        {'choice': 'Python has a simple and easily understandable syntax.', 'question_id': 2},
        {'choice': 'Python has a large community support in the field of artificial intelligence.', 'question_id': 2},
        {'choice': 'All of the above.', 'question_id': 2},
        {'choice': 'TensorFlow', 'question_id': 3},
        {'choice': 'PyTorch', 'question_id': 3},
        {'choice': 'Scikit-Learn', 'question_id': 3},
        {'choice': 'All of the above.', 'question_id': 3},
        {'choice': 'Through evaluation with test data and adjusting model parameters.', 'question_id': 4},
        {'choice': 'By changing the programming language used.', 'question_id': 4},
        {'choice': 'Ignoring user feedback.', 'question_id': 4},
        {'choice': 'All of the above are correct.', 'question_id': 4},
        {'choice': 'Python is not used in developing NLP applications.', 'question_id': 5},
        {'choice': 'Python provides libraries like NLTK and spaCy for natural language processing.', 'question_id': 5},
        {'choice': 'Python is only suitable for developing computer vision applications.', 'question_id': 5},
        {'choice': 'Another programming language is more effective for NLP.',
            'question_id': 5},
    ]

    question_correct_choice_datas = [
        {'question_id': 1, 'choice_id': 1},
        {'question_id': 2, 'choice_id': 8},
        {'question_id': 3, 'choice_id': 12},
        {'question_id': 4, 'choice_id': 13},
        {'question_id': 5, 'choice_id': 18},
    ]

    existing_user = User.query.filter_by(
        username=user_data['username']).first()
    if not existing_user:
        user = User(username=user_data['username'],
                    password=user_data['password'])
        db.session.add(user)
        
        for question_data in questions_data:
            question = Question(question=question_data['question'])
            db.session.add(question)

        for choice_data in choices_data:
            choice = Choice(
                choice=choice_data['choice'], question_id=choice_data['question_id'])
            db.session.add(choice)

        for question_correct_choice_data in question_correct_choice_datas:
            question_correct_choice = QuestionCorrectChoice(
                question_id=question_correct_choice_data['question_id'], correct_choice_id=question_correct_choice_data['choice_id'])
            db.session.add(question_correct_choice)

    db.session.commit()

# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print("ASdSDASDASDASDASDASDASD")
#         questions, choices, question_correct_choice = init_question_data()
#         # db.session.add()
#         print('Created Database!')
