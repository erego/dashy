"""Application entry point."""

from Predilectura import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5070, debug=True)
