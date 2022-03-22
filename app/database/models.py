from app.extensions import db
from werkzeug.security import generate_password_hash
from sqlalchemy import event


class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    data_nascimento = db.Column(db.String(10), nullable=False)

    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(255), nullable=True)


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), nullable=True, unique=True)
    telefone = db.Column(db.String(255), nullable=False)


class Endereco(db.Model):
    __tablename__ = "enderecos"

    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String(255), nullable=False)
    numero = db.Column(db.String(255), nullable=False)
    bairro = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(255), nullable=False)
    cidade = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(255), nullable=False)
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
    )
    cliente = db.relationship("Cliente", foreign_keys=cliente_id)


class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)
    meio_pagamento = db.Column(db.String(255), nullable=False)
    troco = db.Column(db.String(255), nullable=True)

    numero_cartao = db.Column(db.String(255), nullable=True)
    nome_impresso_cartao = db.Column(db.String(255), nullable=True)
    validade = db.Column(db.String(255), nullable=True)
    cvv = db.Column(db.String(255), nullable=True)
    apelido = db.Column(db.String(255), nullable=True)
    cpf_cnpj_titular = db.Column(db.String(255), nullable=True)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
    )
    cliente = db.relationship("Cliente", foreign_keys=cliente_id)


class Marmita(db.Model):
    __tablename__ = "marmitas"

    id = db.Column(db.Integer, primary_key=True)
    nome_prato = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(255), nullable=False)  # comum, fit, low carb
    tamanhos = db.Column(db.String(255), nullable=False)
    preco = db.Column(db.String(255), nullable=False)


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)
    observacao = db.Column(db.String(255), nullable=True)

    funcionario_id = db.Column(
        db.Integer,
        db.ForeignKey("funcionarios.id", ondelete="CASCADE"),
        nullable=False,
    )
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id", ondelete="CASCADE"),
        nullable=False,
    )
    endereco_id = db.Column(
        db.Integer,
        db.ForeignKey("enderecos.id", ondelete="CASCADE"),
        nullable=False,
    )
    funcionario = db.relationship("Funcionario", foreign_keys=funcionario_id)
    cliente = db.relationship("Cliente", foreign_keys=cliente_id)
    endereco = db.relationship("Endereco", foreign_keys=endereco_id)


class Bebida(db.Model):
    __tablename__ = "bebidas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.String(255), nullable=True)
    preco = db.Column(db.String(255), nullable=False)

    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False,
    )
    pedido = db.relationship("Pedido", foreign_keys=pedido_id)


class PedidoMarmita(db.Model):
    __tablename__ = "pedidos_marmitas"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos.id", ondelete="CASCADE"),
        nullable=False,
    )
    pedido = db.relationship("Funcionario", foreign_keys=pedido_id)

    quantidade_marmita = db.Column(db.String(255), nullable=False)
    marmita_id = db.Column(
        db.Integer,
        db.ForeignKey("marmitas.id", ondelete="CASCADE"),
        nullable=False,
    )
    bebida_id = db.Column(
        db.Integer,
        db.ForeignKey("bebidas.id", ondelete="CASCADE"),
        nullable=False,
    )
    quantidade_bebida = db.Column(db.String(255), nullable=False)
    marmita = db.relationship("Marmita", foreign_keys=marmita_id)
    bebida = db.relationship("Bebida", foreign_keys=bebida_id)


class PagamentoMarmita(db.Model):
    __tablename__ = "pagamentos_marmitas"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), nullable=False)
    pedido_marmita_id = db.Column(
        db.Integer,
        db.ForeignKey("pedidos_marmitas.id", ondelete="CASCADE"),
        nullable=False,
    )
    pedido_marmita = db.relationship("PedidoMarmita", foreign_keys=pedido_marmita_id)


@event.listens_for(Funcionario, "before_insert")
def encriptar_senha(mapper, connect, target):
    target.senha = generate_password_hash(target.senha)
