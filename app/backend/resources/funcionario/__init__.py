from app.backend.resources.funcionario.resource import *


def init_api(api):

    api.add_resource(ApiRegistrar, "/registrar", endpoint="registrar")
    api.add_resource(ApiLogin, "/login", endpoint="login")
