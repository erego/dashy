from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_pymongo import PyMongo

login_manager = LoginManager()
mongo = PyMongo()

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Predilectura"
    Bootstrap(app)
    login_manager.init_app(app)
    mongo.init_app(app)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        from . import auth

        app.register_blueprint(auth.auth_bp)

        # Import Dash application
        from .tableros.datos import init_dashboard
        app = init_dashboard(app)

        return app
