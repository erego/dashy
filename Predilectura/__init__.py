from flask import Flask
from flask_bootstrap import Bootstrap

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config["MONGO_URI"] = "mongodb://localhost:27017/Predilectura"
    Bootstrap(app)
    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        from .tableros.datos import init_dashboard
        app = init_dashboard(app)

        return app