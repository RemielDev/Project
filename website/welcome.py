from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from .models import User, School
from . import db
from flask_login import login_user, login_required, logout_user, current_user



welcome = Blueprint('welcome', __name__)



# Login Route
@welcome.route('/', methods=['GET', 'POST'])
def welcome_page():
 
    return render_template("welcome.html")
