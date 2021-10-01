from flask import Blueprint

# https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
views = Blueprint('views', __name__, url_prefix ='/')


@views.route('/')
def home():
    return '<h1> Home </h1>'
