from . import db, login_manager

@login_manager.user_loader
def load(user_id):
    return StudyEvent.query.get(int(user_id))

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
    start_time = db.Column(db.String(100), nullable=False)
    end_time = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(255), nullable=True)

