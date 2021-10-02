from flask import Blueprint,render_template

auth = Blueprint('auth', __name__, url_prefix='/')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return 'Logout'

@auth.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')
