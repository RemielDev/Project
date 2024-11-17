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
    profile_picture = db.Column(db.String(150), nullable=True)  # New field

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    schoolId = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ForeignKey to User
    time_stamp = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    creator = db.relationship('User', backref='threads', lazy=True)  # Relationship to User

    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(1000))
    time_stamp = db.Column(db.DateTime(timezone=True), default=func.now())

