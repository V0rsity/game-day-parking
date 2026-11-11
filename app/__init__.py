# Contains code to create the app
from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
