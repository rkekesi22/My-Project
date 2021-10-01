from flask import Blueprint

# https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/login')
def login():
    return '<h1>Login</h1>'


@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'


@auth.route('/sign-up')
def sign_up():
    return '<h1>Sign up</h1>'