# Contains code to create the app
import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "Purdue")  # Set the secret to something new and unique in production

    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
