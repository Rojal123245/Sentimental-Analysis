from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import user_info
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

# route for the /login page in the website
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # getting the user email from the login form
        password = request.form.get('password')  # getting the user password from the login form

        user = user_info.query.filter_by(email=email).first()  # checking if the user email is in the database
        if user:
            if check_password_hash(user.password, password):  # checking in the database if the user password is correct
                flash('Logged in successfully!', category='success')  # to show the success messagesss
                login_user(user, remember=True)
                return redirect(url_for('views.user', user=current_user))  # redirecting to user page if the login is successful
            else:
                flash('Incorrect password, try again.', category='error')  # user password is incorrect
        else:
            flash('Email does not exist.', category='error')  # if the email does not exist in the database
    return render_template("login.html", user=current_user)


# route for /logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')  # to show the success messages
    return redirect(url_for('views.about'))  # redirecting to about page if the logout is successful

# route for the /register page in the website
@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email')  # getting the user email from the signup form
        name = request.form.get('name')  # getting the user name from the signup form
        password = request.form.get('password')  # getting the user password from the signup form

        user = user_info.query.filter_by(email=email).first()  # checking if the user email is in the database
        if user:
            flash('Email already exists.', category='error')  # in case the user email already exists in the database
        elif len(email) < 4:  # condition for email length
            flash("Email must be greater than 4 characters.", category='error')
        elif len(name) < 2:  # condition for name length
            flash("Name must be greater than 2 characters.", category='error')
        elif len(password) < 7:  # condition for password length
            flash("Password must be greater than 7 characters.", category='error')
        else:
            # assignment of the user information into the variable new_user
            new_user = user_info(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)  # inserting the new user information into the database
            db.session.commit()  # to update the database
            flash("Account created.", category='success')  # to show the success message
            return redirect(url_for('views.about'))
    return render_template("register.html", user=current_user)

# route to /forget the password page in the website
@auth.route('/forget', methods = ['GET'])
def forget():
    return render_template("forgot.html" )
