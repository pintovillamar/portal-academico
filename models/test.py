from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin

import requests
import json

from models.carreras import Carrera, carrera_schema, carreras_schema
from models.usuarios import Usuario, usuario_schema, usuarios_schema, create_usuario
from models.estudiantes import Estudiante, estudiante_schema, estudiantes_schema, create_estudiante
from db.database import db, ma

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

@test_blueprint.route("/test2", methods=["POST"])
@cross_origin()
def test2():
    try:
        # Extract JSON fields:
        data = request.get_json()
        nombres = data.get('nombres')
        apellido_paterno = data.get('apellido_paterno')
        apellido_materno = data.get('apellido_materno')
        carrera_id = data.get('carrera_id')

        # Debugging: Check input data
        print(f"Received data: {data}")

        # Validate json fields:
        if not all([nombres, apellido_paterno, apellido_materno, carrera_id]):
            return jsonify({'message': 'Missing fields'}), 400
        
        # Generate usuario and password:
        usuario = nombres[0].lower() + apellido_paterno.lower() + apellido_materno[0].lower()
        password = usuario + "123"

        # Debugging: Check generated username and password
        print(f"Generated usuario: {usuario}, password: {password}")

        # Create new Usuario:
        new_usuario = Usuario(
            usuario = usuario,
            password = password
        )

        db.session.add(new_usuario)
        db.session.commit()

        # Debugging: Check if Usuario was created
        print(f"New Usuario ID: {new_usuario.id}")

        # Create new Estudiante:
        new_estudiante = Estudiante(
            nombres = nombres,
            apellido_paterno = apellido_paterno,
            apellido_materno = apellido_materno,
            usuario_id = new_usuario.id,
            carrera_id = carrera_id
        )

        db.session.add(new_estudiante)
        db.session.commit()
        
        # Debugging: Check if Estudiante was created
        print(f"New Estudiante ID: {new_estudiante.id}")

        return usuario_schema.jsonify(new_usuario), 201
    
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")  # Print the error for debugging
        return jsonify({'message': str(e)}), 500
