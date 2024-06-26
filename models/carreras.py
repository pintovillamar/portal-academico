# Table view
# id
# nombre

from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import json

from db.database import db, ma
from datetime import datetime

class Carrera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, nombre):
        self.nombre = nombre

class CarreraSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'created_at', 'updated_at')

carrera_schema = CarreraSchema()
carreras_schema = CarreraSchema(many=True)

class CarreraModel:

    # Create carrera
    def create_carrera(self):
        new_carrera = Carrera(
            request.json['nombre']
        )

        db.session.add(new_carrera)
        db.session.commit()
        return carrera_schema.jsonify(new_carrera)
    
    # Read Carrera (Read by id)
    def carrera(self, id):
        carrera = Carrera.query.get(id)
        return carrera_schema.jsonify(carrera)
    
    # Read Carrera (Read all)
    def carreras(self):
        carreras = Carrera.query.all()
        return carreras_schema.jsonify(carreras)
    
    # Update Carrera
    def update_carrera(self, id):
        carrera = Carrera.query.get(id)
        carrera.nombre = request.json['nombre']
        carrera.updated_at = datetime.now()
        db.session.commit()
        return carrera_schema.jsonify(carrera)

    # Delete Carrera
    def delete_carrera(self, id):
        carrera = Carrera.query.get(id)
        db.session.delete(carrera)
        db.session.commit()
        return carrera_schema.jsonify(carrera)
    
# Blueprints (endpoints)

model = CarreraModel()
carrera_blueprint = Blueprint('carreras', __name__)

@carrera_blueprint.route("/create/carrera", methods=["POST"])
@cross_origin()
def create_carrera():
    return model.create_carrera()

@carrera_blueprint.route("/carrera/<id>", methods=["GET"])
@cross_origin()
def carrera(id):
    return model.carrera(id)

@carrera_blueprint.route("/carreras", methods=["GET"])
@cross_origin()
def carreras():
    return model.carreras()

@carrera_blueprint.route("/update/carrera/<id>", methods=["PUT"])
@cross_origin()
def update_carrera(id):
    return model.update_carrera(id)

@carrera_blueprint.route("/delete/carrera/<id>", methods=["DELETE"], endpoint='delete_carrera')
@cross_origin()
def delete_carrera(id):
    return model.delete_carrera(id)