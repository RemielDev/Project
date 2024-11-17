from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    schoolId = db.Column(db.Integer, db.ForeignKey('school.id'))
    notes = db.relationship('Note')

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    title = db.Column(db.String(150), unique=True)
    description = db.Column(db.String(500))  # Added description field
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Added creator field
    time_stamp = db.Column(db.DateTime(timezone=True), default=func.now())  # Added timestamp

    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(1000))
    time_stamp = db.Column(db.DateTime(timezone=True), default=func.now())

