from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_babel import Babel

login_manager = LoginManager()
mongo = PyMongo()
babel = Babel()


def page_not_found(e):
    return render_template('404.jinja2'), 404


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.register_error_handler(404, page_not_found)
    app.config.from_object('config.Config')
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Predilectura"
    babel.init_app(app)
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
