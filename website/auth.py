from flask import Blueprint,render_template,request,flash

auth = Blueprint('auth', __name__, url_prefix='/')

# Now from inside the function we'll check if we are receiving a GET or POST request.
@auth.route('/login', methods=['GET','POST'] )
def login():
    # data = request.form
    # ImmutableMultiDict([('email', 'rolcsi01@hotmail.com'), ('password', '4did@HMcDQJz2CC')])
    # print(data)

    return render_template('login.html')
    # return render_template('login.html', text="This is my webpage")


@auth.route('/logout')
def logout():
    return 'Logout'


@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # ÖTLET: Jelszó ellenőrzés: tartalmaz-e betűt,számot és egyéb karaktert

        # https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/?highlight=flash
        if len(firstName) < 2:
            flash('Túl rövid vezetéknév! Kérlek 1 karakternél többet adj meg.', category='error')
        elif len(lastName) < 2:
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
            flash('Sikeres regisztráció!', category='success')



    return render_template('sign_up.html')


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
