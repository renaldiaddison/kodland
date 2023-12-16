from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql import func
from .models import db, User, Score, Question, Choice, QuestionCorrectChoice
import requests
import json
import datetime

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    current_weather = None
    weather_prediction = None

    try:
        current_weather_response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key=7045af791e474bbdbae64441231612&q=Jakarta&days=0')
        current_weather_response.raise_for_status()
        weather_data = current_weather_response.json()

        current_date_time = datetime.datetime.now().strftime(
            '%A, %d %B %Y')
        morning_temp = weather_data['forecast']['forecastday'][0]['hour'][6]['temp_c']
        night_temp = weather_data['forecast']['forecastday'][0]['hour'][21]['temp_c']

        current_weather = {'city_name': 'Jakarta', 'current_date_time': current_date_time,
                           'morning_temp': morning_temp, 'night_temp': night_temp}

    except requests.exceptions.RequestException as err:
        current_weather = None
        flash("Error Occured!", category='error')

    if request.method == 'POST':
        try:
            cityName = request.form.get('city-name')
            weather_prediction_response = requests.get(
                f'https://api.weatherapi.com/v1/forecast.json?key=7045af791e474bbdbae64441231612&q={cityName}&days=3')
            weather_prediction_response.raise_for_status()

            weather_prediction = weather_prediction_response.json()
        except requests.exceptions.RequestException as err:
            weather_prediction = None
            flash("Error Occured!", category='error')

    return render_template("home.html", user=current_user, weather_prediction=weather_prediction, current_weather=current_weather)


@views.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():

    questions = Question.query.order_by(func.random()).all()
    
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.date.asc()).all()

    if request.method == 'POST':
        total_score = 0
        for question in questions:
            checked_choices = request.form.getlist(f'choiceRadio{question.id}')
            if (len(checked_choices) != 0):
                question_correct_choice = int(QuestionCorrectChoice.query.filter_by(
                    question_id=question.id).first().correct_choice_id)
                selected_choice = int(checked_choices[0])
                if (question_correct_choice == selected_choice):
                    total_score += 1

        score = total_score/len(questions) * 100
        new_score = Score(score=score, user_id=current_user.id)
        db.session.add(new_score)
        db.session.commit()
        scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.date.asc()).all()

    return render_template("quiz.html", user=current_user, questions=questions, scores=scores)


@views.route('/leaderboard', methods=['GET'])
@login_required
def leaderboard():
    high_scores = db.session.query(User.username, Score.score, Score.date).join(Score).order_by(Score.score.desc()).limit(20).all()

    return render_template("leaderboard.html", user=current_user, high_scores=high_scores)
