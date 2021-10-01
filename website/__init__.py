from flask import Flask



def create_app():
    app = Flask(__name__)

    # https://stackoverflow.com/questions/34902378/where-do-i-get-a-secret-key-for-flask
    # Get the random string for secret key:
    # >>> import secrets
    # >>> secrets.token_urlsafe(16) OR secrets.token_hex(16)

    # The secret key is needed to keep the client-side sessions secure.
    app.secret_key = 'yhGT3ylGryGTCasbc7yoZQ'

    from .views import views
    from .auth import auth

    # Registering Blueprints
    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app

