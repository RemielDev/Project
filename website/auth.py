from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, School

from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user




auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    schools = ["Pierce College", "UCI", "UCLA", "CSU Long Beach"]  # List of schools
    print("Schools list being passed:", schools)  # Debugging

    if request.method == 'POST':
        email = request.form.get('email')
        schoolId = request.form.get('schoolId')  # Capturing the selected school
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        school = School.query.filter_by(name=schoolId).first()
        if not school: 
           db.session.add(School(name=schoolId))
           db.session.commit()
        print(schoolId)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
           
            new_user = User(
                        email=email, 
                        first_name=first_name,
                        schoolId=schoolId, 
                        password=generate_password_hash(
                        password=password1, method='scrypt')
                            )
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    # Pass the schools list to the template
    return render_template("sign_up.html", user=current_user, schools=schools)




@auth.route('/test', methods=['GET', 'POST'])
def test():

    if request.method == 'POST':
        data = request.form.get('data')
        print(data)
