# Table view
# usuario
# contraseña

from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import json

from db.database import db, ma
from datetime import datetime

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __init__(self, usuario ,password):
        self.usuario = usuario
        self.password = password
        
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'usuario', 'password', 'created_at', 'updated_at')
        
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

class UsuarioModel:
    
    # Create usuario
    def create_usuario(self):
        new_usuario = Usuario(
            request.json['usuario'],
            request.json['password']
        )
        
        db.session.add(new_usuario)
        db.session.commit()
        return usuario_schema.jsonify(new_usuario)
    
    # Read usuario (Read by id)
    def usuario(sefl, id):
        usuario = Usuario.query.get(id)
        return usuario_schema.jsonify(usuario)
    
    # Read usuario (Read all)
    def usuarios(self):
        usuarios = Usuario.query.all()
        return usuarios_schema.jsonify(usuarios)
    
    # Update usuario
    def update_usuario(self, id):
        usuario = Usuario.query.get(id)
        usuario.usuario = request.json['usuario']
        usuario.password = request.json['password']
        usuario.updated_at = datetime.now()
        db.session.commit()
        return usuario_schema.jsonify(usuario)
    
    # Delete usuario
    def delete_usuario(self, id):
        usuario = Usuario.query.get(id)
        db.session.delete(usuario)
        db.session.commit()
        return usuario_schema.jsonify(usuario)
# Blueprints (endpoints)

model = UsuarioModel()
usuario_blueprint = Blueprint('usuarios', __name__)

@usuario_blueprint.route("/create/usuario", methods=["POST"])
@cross_origin()
def create_usuario():
    return model.create_usuario()

@usuario_blueprint.route("/usuario/<id>", methods=["GET"])
@cross_origin()
def usuario(id):
    return model.usuario(id)

@usuario_blueprint.route("/usuarios", methods=["GET"])
@cross_origin()
def usuarios():
    return model.usuarios()

@usuario_blueprint.route("/update/usuario/<id>", methods=["PUT"])
@cross_origin()
def update_usuario(id):
    return model.update_usuario(id)

@usuario_blueprint.route("/delete/usuario/<id>", methods=["DELETE"], endpoint='delete_usuario')
@cross_origin()
def delete_usuario(id):
    return model.delete_usuario(id)