from flask import Blueprint,render_template,request,flash

# https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
auth = Blueprint('auth', __name__, url_prefix='/')


@auth.route('/login', methods=['GET','POST'])
def login():

    return render_template("login.html",)


@auth.route('/logout')
def logout():
    return '<h1>Logout</h1>'


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        fullName = request.form.get('fullName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fullName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            flash('Account created!', category='success')

    return render_template("sign_up.html")