from dynaconf import FlaskDynaconf
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()


def init_app(app):
    FlaskDynaconf(app)
    app.config["DEBUG"] = True
    db.init_app(app)

    app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "test"
    app.config["JWT_ACCESS_CSRF_COOKIE_NAME"] = "test"
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_SESSION_COOKIE"] = False
    jwt.init_app(app)

    CORS(app)
    Migrate(app, db)

    from app.database.models import Funcionario

    @app.shell_context_processor
    def context_processor():

        return dict(app=app, db=db, Funcionario=Funcionario)
