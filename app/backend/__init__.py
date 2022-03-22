from app.backend.resources import funcionario
from flask_restful import Api
from flask import Blueprint


bp = Blueprint("api", __name__, url_prefix="/api/v1")
bp_funcionario = Blueprint("api_funcionario", __name__)

api_funcionario = Api(bp_funcionario)


def init_app(app):

    bp.register_blueprint(bp_funcionario)
    funcionario.init_api(api_funcionario)
    app.register_blueprint(bp)
