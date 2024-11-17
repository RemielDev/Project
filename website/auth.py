from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from .models import User, School
from . import db
from flask_login import login_user, login_required, logout_user, current_user

schools = [
    "Allan Hancock College",
    "American River College",
    "Antelope Valley College",
    "Bakersfield College",
    "Barstow Community College",
    "Berkeley City College",
    "Butte College",
    "Cabrillo College",
    "Cañada College",
    "Cerritos College",
    "Chabot College",
    "Chaffey College",
    "Citrus College",
    "City College of San Francisco",
    "Clovis Community College",
    "Coastline College",
    "College of Alameda",
    "College of Marin",
    "College of San Mateo",
    "College of the Canyons",
    "College of the Desert",
    "College of the Redwoods",
    "College of the Sequoias",
    "Columbia College",
    "Contra Costa College",
    "Copper Mountain College",
    "Cosumnes River College",
    "Crafton Hills College",
    "Cuesta College",
    "Cuyamaca College",
    "Cypress College",
    "De Anza College",
    "Diablo Valley College",
    "East Los Angeles College",
    "El Camino College",
    "Evergreen Valley College",
    "Feather River College",
    "Folsom Lake College",
    "Foothill College",
    "Fresno City College",
    "Fullerton College",
    "Gavilan College",
    "Glendale Community College",
    "Golden West College",
    "Grossmont College",
    "Hartnell College",
    "Imperial Valley College",
    "Irvine Valley College",
    "Lake Tahoe Community College",
    "Laney College",
    "Las Positas College",
    "Lassen College",
    "Long Beach City College",
    "Los Angeles City College",
    "Los Angeles Harbor College",
    "Los Angeles Mission College",
    "Los Angeles Pierce College",
    "Los Angeles Southwest College",
    "Los Angeles Trade-Tech College",
    "Los Angeles Valley College",
    "Los Medanos College",
    "Madera Community College",
    "Marin College",
    "Merritt College",
    "MiraCosta College",
    "Mission College",
    "Modesto Junior College",
    "Monterey Peninsula College",
    "Mt. San Antonio College",
    "Mt. San Jacinto College",
    "Napa Valley College",
    "Norco College",
    "Ohlone College",
    "Orange Coast College",
    "Oxnard College",
    "Palo Verde College",
    "Palomar College",
    "Pasadena City College",
    "Porterville College",
    "Reedley College",
    "Rio Hondo College",
    "Riverside City College",
    "Saddleback College",
    "San Bernardino Valley College",
    "San Diego City College",
    "San Diego Mesa College",
    "San Diego Miramar College",
    "San Francisco City College",
    "San Joaquin Delta College",
    "San Jose City College",
    "Santa Ana College",
    "Santa Barbara City College",
    "Santa Monica College",
    "Santa Rosa Junior College",
    "Santiago Canyon College",
    "Shasta College",
    "Sierra College",
    "Skyline College",
    "Solano Community College",
    "Southwestern College",
    "Taft College",
    "Ventura College",
    "Victor Valley College",
    "West Hills College Coalinga",
    "West Hills College Lemoore",
    "West Los Angeles College",
    "West Valley College",
    "Woodland Community College",
    "Yuba College"
]


auth = Blueprint('auth', __name__)
thread = Blueprint('thread', __name__)

# Allowed file extensions for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure the uploads directory exists
UPLOAD_FOLDER = os.path.join('static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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

    if request.method == 'POST':
        
        email = request.form.get('email').lower()
        first_name = request.form.get('firstName')
        school_name = request.form.get('schoolId')  # Fetch selected school
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        profile_picture = request.files.get('profilePicture')

        print(f"Selected school: {school_name}")  # Debugging


        if not school_name or school_name not in schools:
            flash('Invalid school selected.', category='error')
            return render_template("sign_up.html", user=current_user, schools=schools)


        # Check if school exists
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
            # Save the profile picture or assign a default
            profile_picture_url = '/static/images/default-profile.png'
            if profile_picture and allowed_file(profile_picture.filename):
                try:
                    filename = secure_filename(profile_picture.filename)
                    profile_picture_path = os.path.join(UPLOAD_FOLDER, filename)
                    profile_picture.save(profile_picture_path)
                    profile_picture_url = f'/static/images/{filename}'
                except Exception as e:
                    flash(f"Error saving profile picture: {str(e)}", category='error')

            new_user = User(
                email=email,
                first_name=first_name,
                schoolId=school.id,
                password=password1,
                profile_picture=profile_picture_url
            )
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
