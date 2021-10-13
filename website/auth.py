from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt

from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__, url_prefix='/')


bcrypt = Bcrypt()

# Now from inside the function we'll check if we are receiving a GET or POST request.
@auth.route('/login', methods=['GET','POST'] )
def login():
    # data = request.form
    # ImmutableMultiDict([('email', 'rolcsi01@hotmail.com'), ('password', '4did@HMcDQJz2CC')])
    # print(data)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/?highlight=query%20filter_by
        user = User.query.filter_by(email=email).first()
        if user:
            # Összehasonlítja a meglévő jelszavakat a jelenlegivel
            # if check_password_hash(user.password,password):
            if bcrypt.check_password_hash(user.password, password):
                flash('Sikeres bejelentkezés!', category='success')
                # https://flask-login.readthedocs.io/en/latest/#flask_login.login_user
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Helytelen jelszó, kérem próbálja meg újból.', category='error')
        else:
            flash('Email cím nem létezik!', category='error')

    return render_template('login.html', user=current_user)
    # return render_template('login.html', text="This is my webpage")


# @login_required -> Csak akkor történhet meg, ha a felhasználó be van jelentkezve
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        last_name = request.form.get('lastName')
        first_name = request.form.get('firstName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # ÖTLET: Jelszó ellenőrzés: tartalmaz-e betűt,számot és egyéb karaktert

        # https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/?highlight=flash
        user = User.query.filter_by(email=email).first()
        if user:
            flash('A megadott email cím már létezik!', category='error')
        elif len(last_name) < 2:
            flash('Túl rövid vezetéknév! Kérlek 1 karakternél többet adj meg.', category='error')
        elif len(first_name) < 2:
            flash('Túl rövid keresztnév! Kérlek 1 karakternél többet adj meg.', category='error')
        elif len(email) < 4:
            flash('Túl rövid email cím! Kérlek 3 karakternél többet adj meg.', category='error')
        elif len(password1) < 5:
            flash('Túl rövid jelszó! Kérlek 4 karakternél többet adj meg.', category='error')
        elif not password_control(password1):
            flash('A jelszó helytelen!', category='error')
        elif password1 != password2:
            flash('A jelszavak nem egyeznek, kérlek próbáld meg újból.', category='error')
        else:



            # https://stackoverflow.com/questions/23432478/why-is-the-output-of-werkzeugs-generate-password-hash-not-constant
            # method$salt$hash
            # new_user = User(last_name=last_name,first_name=first_name,email=email,password= generate_password_hash(password1,'sha256',salt_length=16))
            new_user = User(last_name=last_name, first_name=first_name, email=email,
                            password=bcrypt.generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Sikeres regisztráció!', category='success')
            # Returns a response object (a WSGI application) that, if called, redirects the client to the target location.
            # To build a URL to a specific function, use the url_for() function.
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)


# Jelsó ellenőrzés
def password_control(jelszo):
    betu = False
    szam = False
    egyeb = False
    # k, mint karakter
    for k in jelszo:
        if k.isspace():
            return False
        elif k.isalnum():
            betu = True
            szam = True
        elif not k.isalnum():
            egyeb = True

    if betu and szam and egyeb:
        return True

    return False
