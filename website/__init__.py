from flask import Flask
import secrets
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



# https://flask-sqlalchemy.palletsprojects.com/en/2.x/
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # User could look at the contents of your cookie but not modify it, unless they know the secret key used for signing.
    # Set secret key in Flask
    app.secret_key = secrets.token_urlsafe(16)
    # print(app.secret_key)

    # SQLAlchemy located here -> sqlite:///{DB_NAME}
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    # If you check the rules registered on the application
    # print(app.url_map)

    from .models import User

    # https://flask-login.readthedocs.io/en/latest/#login-example
    # például hogy hogyan lehet betölteni egy felhasználót az azonosítóból, hová kell küldeni a felhasználókat, amikor bejelentkezniük kell, és hasonlók.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Adatbázis létrejött!')