from db import db
from datetime import datetime
from flask_login import UserMixin


class EquipamentosTecnicos(db.Model):
    __tablename__ = 'equipamentos_tecnicos'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    garantia = db.Column(db.Float, nullable=False, default=0.0)
    fabricante_marca = db.Column(db.String)
    modelo = db.Column(db.String)
    numero_serie = db.Column(db.Float)
    data_fabricacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    validade = db.Column(db.Boolean)
    condicao = db.Column(db.String)
    localizacao = db.Column(db.String)
    patrimonio = db.Column(db.String)
    quantidade = db.Column(db.Integer)

class EquipamentosTi(db.Model):
    __tablename__ = 'equipamentos_ti'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    garantia = db.Column(db.Float, nullable=False, default=0.0)
    fabricante_marca = db.Column(db.String)
    modelo = db.Column(db.Boolean, nullable=False, default=False)
    numero_serie = db.Column(db.Float)
    data_fabricacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    validade = db.Column(db.Boolean)
    condicao = db.Column(db.String)
    localizacao = db.Column(db.String)
    patrimonio = db.Column(db.String)
    quantidade = db.Column(db.Integer)

class EquipamentosGamer(db.Model):
    __tablename__ = 'equipamentos_gamers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    categoria = db.Column(db.String)
    quantidade = db.Column(db.Integer)

class NotasFiscais(db.Model):
    __tablename__ = 'notas_fiscais'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    descricao_itens = db.Column(db.String)
    numero_nf = db.Column(db.Float, nullable=False, default=0.0)
    data_fabricacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    fornecedor = db.Column(db.String)
    cnpj = db.Column(db.Float, nullable=False, default=0.0)
    quantidade = db.Column(db.Integer)
    valor_total = db.Column(db.Float, nullable=False, default=0.0)

class EquipamentosConsumo(db.Model):
    __tablename__ = 'equipamentos_consumo'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    garantia = db.Column(db.Float, nullable=False, default=0.0)
    cor = db.Column(db.String)
    fabricante_marca = db.Column(db.String)
    modelo = db.Column(db.Boolean, nullable=False, default=False)
    numero_serie = db.Column(db.Float, nullable=False, default=0.0)
    data_fabricacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    validade = db.Column(db.Boolean)
    condicao = db.Column(db.String)
    localizacao = db.Column(db.String)
    patrimonio = db.Column(db.String)
    quantidade = db.Column(db.Integer)

class RelatorioAtividade(db.Model):
    __tablename__ = 'relatorio_atividade'
    id = db.Column(db.Integer, primary_key=True)
    aluno = db.Column(db.String)
    atividade = db.Column(db.String)
    professor_responsavel = db.Column(db.String)
    data = db.Column(db.DateTime, nullable=False, default=datetime.now)
    observacao = db.Column(db.String)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='visitante')  # visitante, tecnico, admin


