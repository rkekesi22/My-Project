from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    last_name = db.Column(db.String(60))
    first_name = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    projects = db.relationship('Projects')
    tasks = db.relationship('Tasks')


class Projects(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20))
    active = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks = db.relationship('Tasks')

    def __init__(self, project, active, user_id):
        self.project_name = project
        self.active = active
        self.user_id = user_id

    def __repr__(self):
        return '<Project {}>'.format(self.project_name)


class Tasks(db.Model):
    task_id = db.Column(db.Integer,primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    task_name = db.Column(db.String(60))
    status = db.Column(db.Boolean, default=False)
    task_time = db.Column(db.String(60))
    description = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, project_id, task_name, status, task_time, description,user_id):
        self.project_id = project_id
        self.task_name = task_name
        self.status = status
        self.task_time = task_time
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<Task {}>'.format(self.task_name)
