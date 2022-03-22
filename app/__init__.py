from flask import Flask
from app import extensions, backend


def create_app():
    app = Flask(__name__)
    extensions.init_app(app)
    backend.init_app(app)
    return app
