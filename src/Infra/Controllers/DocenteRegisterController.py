from flask import request, jsonify
from ..Models.EstudianteModels import db, Estudiantes
from datetime import datetime
from .Errors import ErrorClient as errorCliente
from .Errors import ErrorServer as errorServer
import bcrypt
from sqlalchemy.exc import IntegrityError

def registrarEstudiantesDocente():
    data = request.get_json()
    required_fields = ["correo_estudiante", "contrasenia"]

    if not all(field in data for field in required_fields):
        raise errorCliente.BadRequest(description="Todos los campos son obligatorios")
    
    # Hashear la contraseña antes de guardar
    contrasenia_hash = bcrypt.hashpw(data["contrasenia"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    estudiante = Estudiantes(
        correo_estudiante = data["correo_estudiante"],
        contrasenia = contrasenia_hash,
        fecha_registro = datetime.now(),
    )
    try:
        db.session.add(estudiante)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        mensaje_bd = str(e.orig)  # Mensaje original de la base de datos
        if "unique constraint" in mensaje_bd.lower() or "duplicate" in mensaje_bd.lower():
            raise errorCliente.BadRequest(description="Ya existe un estudiante con ese correo electrónico.")
        else:
            raise errorCliente.BadRequest(description=f"Error en la base de datos: {mensaje_bd}")
    return jsonify({"status": 201,
                    "message": "Estudiante creado exitosamente", 
                    "data": estudiante.to_dict()}), 201
