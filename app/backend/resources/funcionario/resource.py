from base64 import b64decode, b64encode
from datetime import timedelta

from app.database.models import Funcionario
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from flask_restful import Resource, request
from werkzeug.security import check_password_hash


def msg(type, msg, code):
    message = jsonify({"type": type, "msg": msg, "code": code})
    response = make_response(message, code)
    # response.headers["Content-Type"] = "application/json"
    return response


def login_msg(type, msg, code, token):
    message = jsonify(
        {"type": type, "msg": msg, "code": code, "access_token": token}
    )
    response = make_response(message, code)
    response.headers["Content-Type"] = "application/json"
    return response


def encodeB64(self):
    self_bytes = b64encode(f"{self}".encode("ascii"))
    return self_bytes.decode("ascii")


def build_token(id):
    identity = {"85ee": encodeB64(id), "49cc": "1b568fc621705f43"}
    expires = timedelta(minutes=60)
    token = create_access_token(identity=identity, expires_delta=expires)
    return token


class ApiRegistrar(Resource):
    def post(self):
        # args = registrar_parser()
        # validation = registrar_args(args)
        # if validation:
        # return validation

        # funcionario, token = registrar_funcionario(args)
        # db.session.add(funcioario)
        try:
            # db.session.commit()
            return msg("success", "Cadastro realizado com sucesso.", 201)
        except Exception as e:
            # logging.critical(str(e))
            # db.session.rollback()
            return msg("error", "Não foi possível concluir o cadastro!", 500)


class ApiLogin(Resource):
    def get(self):
        if not request.headers.get("Authorization"):
            return msg("error", "Não tente burlar o login!", 401)
        basic, code = request.headers["Authorization"].split(" ")
        if not basic.lower() == "basic":
            return msg("error", "Não tente burlar o login!", 401)

        email, senha = b64decode(code).decode().split(":")

        funcionario = Funcionario.query.filter_by(email=email).first()
        if not funcionario:
            return msg("error", "E-mail não encontrado!", 401)
        if not check_password_hash(funcionario.senha, senha):
            return msg("error", "Senha incorreta!", 401)

        token = build_token(id=funcionario.id)
        return login_msg("success", "Login realizado com sucesso.", 200, token)
