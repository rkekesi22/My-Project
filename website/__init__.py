from flask import Flask
import secrets

def create_app():
    app = Flask(__name__)

    # User could look at the contents of your cookie but not modify it, unless they know the secret key used for signing.
    # Set secret key in Flask
    app.secret_key = secrets.token_urlsafe(16)
    # print(app.secret_key)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    # If you check the rules registered on the application
    # print(app.url_map)

    return app