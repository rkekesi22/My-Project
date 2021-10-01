from flask import Blueprint,render_template

# https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
views = Blueprint('views', __name__, url_prefix ='/')


@views.route('/')
def home():
    return render_template("home.html")
