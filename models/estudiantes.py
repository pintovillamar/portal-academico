# Table view
# id
# nombres
# apellido paterno
# apellido materno
# usuario id
# carrera id

from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import json

from db.database import db, ma
from datetime import datetime

from models.carreras import Carrera, carrera_schema, carreras_schema

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(256), nullable=False)
    apellido_paterno = db.Column(db.String(256), nullable=False)
    apellido_materno = db.Column(db.String(256), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    carrera_id = db.Column(db.Integer, db.ForeignKey('carrera.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    def __init__(self, nombres, apellido_paterno, apellido_materno, usuario_id, carrera_id):
        self.nombres = nombres
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.usuario_id = usuario_id
        self.carrera_id = carrera_id

class EstudianteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombres', 'apellido_paterno', 'apellido_materno', 'usuario_id', 'carrera_id', 'created_at', 'updated_at')

estudiante_schema = EstudianteSchema()
estudiantes_schema = EstudianteSchema(many=True)

class EstudianteModel:

    # Create estudiante
    def create_estudiante(self):
        new_estudiante = Estudiante(
            request.json['nombres'],
            request.json['apellido_paterno'],
            request.json['apellido_materno'],
            request.json['usuario_id'],
            request.json['carrera_id']
        )
        
        db.session.add(new_estudiante)
        db.session.commit()
        return estudiante_schema.jsonify(new_estudiante)
    
    # Read estudiante (Read by id)
    def estudiante(self, id):
        estudiante = Estudiante.query.get(id)
        return estudiante_schema.jsonify(estudiante)
    
    # Read estudiante (Read all)
    def estudiantes(self):
        estudiantes = Estudiante.query.all()
        return estudiantes_schema.jsonify(estudiantes)
    
    # Update estudiante
    def update_estudiante(self, id):
        estudiante = Estudiante.query.get(id)
        estudiante.nombres = request.json['nombres']
        estudiante.apellido_paterno = request.json['apellido_paterno']
        estudiante.apellido_materno = request.json['apellido_materno']
        estudiante.usuario_id = request.json['usuario_id']
        estudiante.carrera_id = request.json['carrera_id']
        estudiante.updated_at = datetime.now()
        db.session.commit()
        return estudiante_schema.jsonify(estudiante)
    
    # Delete estudiante
    def delete_estudiante(self, id):
        estudiante = Estudiante.query.get(id)
        db.session.delete(estudiante)
        db.session.commit()
        return estudiante_schema.jsonify(estudiante)
    
    # Frontend requests
    # carrera, y estudiantes en esa carrera

    def get_carreras_with_estudiante_count(self):
        from models.carreras import Carrera  # Assuming Carrera model is in models/carreras.py
        carreras = Carrera.query.all()
        result = []
        for carrera in carreras:
            estudiantes_count = Estudiante.query.filter_by(carrera_id=carrera.id).count()
            result.append({"name": carrera.nombre, "value": estudiantes_count})
        return jsonify(result)

    # lista de estudiantes: get 10 estudiantes

    def get_estudiantes_with_carreras(self):
        estudiantes = Estudiante.query.all()
        result = []
        for estudiante in estudiantes:
            # Fetch the carrera for each estudiante dynamically
            carrera = Carrera.query.filter_by(id=estudiante.carrera_id).first()
            # Ensure carrera is not None before accessing its nombre
            carrera_nombre = carrera.nombre if carrera else 'Unknown'
            # Construct the dictionary in the desired format
            estudiante_info = {
                "id": estudiante.id,
                "nombres": estudiante.nombres,
                "apellido_paterno": estudiante.apellido_paterno,
                "apellido_materno": estudiante.apellido_materno,
                "carrera": carrera_nombre,
            }
            result.append(estudiante_info)

        return jsonify(result)  # Directly return the list of dictionaries
    
# Blueprints (endpoints)

model = EstudianteModel()
estudiante_blueprint = Blueprint('estudiantes', __name__)

@estudiante_blueprint.route("/create/estudiante", methods=["POST"])
@cross_origin()
def create_estudiante():
    return model.create_estudiante()

@estudiante_blueprint.route("/estudiante/<id>", methods=["GET"])
@cross_origin()
def estudiante(id):
    return model.estudiante(id)

@estudiante_blueprint.route("/estudiantes", methods=["GET"])
@cross_origin()
def estudiantes():
    return model.estudiantes()

@estudiante_blueprint.route("/update/estudiante/<id>", methods=["PUT"])
@cross_origin()
def update_estudiante(id):
    return model.update_estudiante(id)

@estudiante_blueprint.route("/delete/estudiante/<id>", methods=["DELETE"])
@cross_origin()
def delete_estudiante(id):
    return model.delete_estudiante(id)

@estudiante_blueprint.route("/estudiantes/carreras", methods=["GET"])
@cross_origin()
def get_estudiantes_with_carreras():
    return model.get_estudiantes_with_carreras()

@estudiante_blueprint.route("/estudiantes/carrera", methods=["GET"])
@cross_origin()
def get_carreras_with_estudiante_count():
    return model.get_carreras_with_estudiante_count()
