from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, School
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
thread = Blueprint('thread', __name__)


# Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').lower()
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('thread.view_threads'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Sign-Up Route
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    schools = ["Pierce College", "UCI", "UCLA", "CSU Long Beach"]  # Example list of schools

    if request.method == 'POST':
        email = request.form.get('email').lower()
        first_name = request.form.get('firstName')
        school_name = request.form.get('schoolId')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the school exists in the database
        school = School.query.filter_by(name=school_name).first()
        if not school:
            school = School(name=school_name)
            db.session.add(school)
            db.session.commit()

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
            new_user = User(email=email, first_name=first_name, school_id=school.id, password=password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('thread.view_threads'))

    return render_template("sign_up.html", user=current_user, schools=schools)

# Logout Route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))
