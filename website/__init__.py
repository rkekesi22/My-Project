from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    # https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask
    # Get the random string for secret key:
    # >>> import secrets
    # >>> secrets.token_urlsafe(16) OR secrets.token_hex(16)

    # The secret key is needed to keep the client-side sessions secure.
    app.secret_key = 'yhGT3ylGryGTCasbc7yoZQ'

    # To Database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    # Registering Blueprints
    app.register_blueprint(views)
    app.register_blueprint(auth)

    from .models import User

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

