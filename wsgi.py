"""Application entry point."""

from flask_pymongo import PyMongo

from Predilectura import init_app

app = init_app()
mongo = PyMongo(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5070, debug=True)