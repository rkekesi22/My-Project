from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    last_name = db.Column(db.String(60), unique=True)
    first_name = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))


class Projects(db.Model):
    project_id = db.Column(db.Integer,primary_key=True)
    project_name = db.Column(db.String(30))
    active = active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Tasks(db.Model):
    task_id = db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    task_name = db.Column(db.String(60))
    status = db.Column(db.Boolean, default=False)
    task_time = db.Column(db.String(60))
    description = db.Column(db.String(250))
