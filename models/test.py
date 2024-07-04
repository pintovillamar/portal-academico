from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import json

from models.carreras import Carrera, carrera_schema, carreras_schema
from models.usuarios import Usuario, usuario_schema, usuarios_schema, create_usuario
from models.estudiantes import Estudiante, estudiante_schema, estudiantes_schema, create_estudiante
from db.database import db, ma
import datetime

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route("/test", methods=["POST"])
@cross_origin()
def test():
    nombres = request.json['nombres']
    apellido_paterno = request.json['apellido_paterno']
    apellido_materno = request.json['apellido_materno']
    usuario = nombres[0].lower() + apellido_paterno.lower() + apellido_materno[0].lower()
    password = nombres[0].lower() + apellido_paterno.lower() + apellido_materno[0].lower() + "123"
    carrera_id = request.json["carrera_id"]
    
    new_usuario = Usuario(
        usuario,
        password,
    )

    db.session.add(new_usuario)
    db.session.commit()

    usuario_id = new_usuario.id

    new_estudiante = Estudiante(
        nombres,
        apellido_paterno,
        apellido_materno,
        usuario_id,
        carrera_id
    )
    
    db.session.add(new_estudiante)
    db.session.commit()


    return usuario_schema.jsonify(new_usuario)

# CRUD de ESTUDIANTES
# Crear un estudiante

@test_blueprint.route("/api/crear-estudiante", methods=["POST"])
@cross_origin()
def crear_estudiante():
    try:
        data = request.get_json()
        nombres = data.get('nombres')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        carrera_id = data.get('carrera_id')

        print(f"Received data: {data}")

        if not all([nombres, apellido_paterno, apellido_materno, carrera_id]):
            return jsonify({'message': 'Missing fields'}), 400
        
        usuario = nombres[0].lower() + apellido_paterno.lower() + apellido_materno[0].lower()
        password = usuario + "123"

        print(f"Generated usuario: {usuario}, password: {password}")

        new_usuario = Usuario(
            usuario = usuario,
            password = password
        )

        db.session.add(new_usuario)
        db.session.commit()

        print(f"New Usuario ID: {new_usuario.id}")

        new_estudiante = Estudiante(
            nombres = nombres,
            apellido_paterno = apellido_paterno,
            apellido_materno = apellido_materno,
            usuario_id = new_usuario.id,
            carrera_id = carrera_id
        )

        db.session.add(new_estudiante)
        db.session.commit()
        
        print(f"New Estudiante ID: {new_estudiante.id}")

        return usuario_schema.jsonify(new_usuario), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500
    

# Update Estudiante

@test_blueprint.route("/api/actualizar-estudiante/<id>", methods=["PUT"])
@cross_origin()
def update_estudiante(id):
    try:
        data = request.get_json()
        nombres = data.get('nombres')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        carrera_id = data.get('carrera_id')

        print(f"Received data: {data}")

        if not all([nombres, apellido_paterno, apellido_materno, carrera_id]):
            return jsonify({'message': 'Missing fields'}), 400
        
        estudiante = Estudiante.query.get(id)

        if not estudiante:
            return jsonify({'message': 'Estudiante not found'}), 404
        
        estudiante.nombres = nombres
        estudiante.apellido_paterno = apellido_paterno
        estudiante.apellido_materno = apellido_materno
        estudiante.carrera_id = carrera_id

        usuario_id = estudiante.usuario_id

        usuario = Usuario.query.get(usuario_id) # FROM USUARIO WHERE ID = usuario_id

        usuario.usuario = nombres[0].lower() + apellido_paterno.lower() + apellido_materno[0].lower()
        usuario.password = usuario.usuario + "123"

        print(f"Updated Estudiante ID: {estudiante.id} with: nombres: {nombres}, apellido_paterno: {apellido_paterno}, apellido_materno: {apellido_materno}, carrera_id: {carrera_id}, usuario_id: {usuario_id}")
        print(f"Updated Usuario ID: {usuario.id} with: usuario: {usuario.usuario}, password: {usuario.password}")

        db.session.commit()

        return estudiante_schema.jsonify(estudiante), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500
    
# Delete Estudiante
@test_blueprint.route("/api/eliminar-estudiante/<id>", methods=["DELETE"])
@cross_origin()
def delete_estudiante(id):
    try:
        estudiante = Estudiante.query.get(id)

        if not estudiante:
            return jsonify({'message': 'Estudiante not found'}), 404

        usuario_id = estudiante.usuario_id

        usuario = Usuario.query.get(usuario_id)

        db.session.delete(estudiante)
        db.session.delete(usuario)
        db.session.commit()

        print(f"Deleted Estudiante ID: {estudiante.id}")
        print(f"Deleted Usuario ID: {usuario.id}")

        return estudiante_schema.jsonify(estudiante), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'message': str(e)}), 500