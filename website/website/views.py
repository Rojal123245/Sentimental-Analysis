import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
# from sqlalchemy import create_engine

views = Blueprint('views', __name__)

# route for the home page
@views.route('/')
def about():
    return render_template("about.html", user=current_user)

# route for the contact page
@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

# route for the dashboard page
@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# For sentiment analysis
nltk.download('vader_lexicon')

# Route for the user page: Sentiment Analysis
@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    if request.method == 'POST':
        # getting the review that the user wants
        review = request.form.get('hotel_review')  # getting the review

        # Sentiment predictor
        sia = SentimentIntensityAnalyzer()
        score = sia.polarity_scores(review)
        if score["neg"] != 0:
            return render_template("user.html", message="🙁 Negative sentiment", review=review, user=current_user)
        else:
            return render_template("user.html", message="🙂 Positive sentiment", review=review, user=current_user)
    return render_template("user.html", user=current_user)

# route for the reviews page
@views.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    if request.method == 'POST':
        # getting the location (city) that the user wants
        location = request.form.get('location')
        # getting the rating that the user wants
        rating = request.form.get('hotel_rating')
        # getting the number of reviews that the user wants
        num_reviews = int(request.form.get('num_reviews'))

        # Connection with the table for the desired city
        ENDPOINT = "nemesisrds.cjmjlsxabz75.us-east-1.rds.amazonaws.com"
        PORT = 3306
        USER = "admin"
        DBNAME = "nemesis_data"
        token = 'passwordRDS'

        conn = pymysql.connect(host=ENDPOINT, user=USER,
                               passwd=token, port=PORT, database=DBNAME)
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT hotelName, user_review, prediction FROM nemesis_data.nemesishotelAndReviewData WHERE City = %s AND hotelRating = %s LIMIT %s",
                    (location, rating, num_reviews))
        query_results = cur.fetchall()
        print(query_results)
        conn.close()
        return render_template("reviews.html", query_results=query_results, user=current_user, location=location, hotel_rating=rating, num_reviews=num_reviews)

    if request.method == 'GET':
        return render_template("reviews.html", user=current_user)
