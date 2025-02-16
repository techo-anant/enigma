from . import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):  # Change db.model to db.Model
    # Each attribute of the class (e.g., username, id) corresponds to a column in the database table.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    Level = db.Column(db.Integer, nullable=False, default= 0)
    experience = db.Column(db.Integer, nullable=False, default= 0)

 
class StudyEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    reminder = db.Column(db.Boolean, default=True)
    link = db.Column(db.String(255), nullable=True)
 
class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(255), nullable=True)

