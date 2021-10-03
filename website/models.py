from . import db
from flask_login import UserMixin
# osztály flask_login.UserMixin[forrás]
# Ez alapértelmezett megvalósításokat biztosít a Flask-Login által a felhasználói objektumoktól elvárt módszerekhez.


# To create the initial database, just import the db object from an interactive Python shell and run the SQLAlchemy.create_all() method
# to create the tables and database:
# >>> from yourapplication import db
# >>> db.create_all()
class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(60), unique=True)
    last_name = db.Column(db.String(60), unique=True)
    email = db.Column(db.String(120), unique=True)
    passwrod = db.Column(db.String(120))