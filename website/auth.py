from flask import Blueprint,render_template

# https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/login')
def login():
    return render_template("login.html",)


@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'


@auth.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")