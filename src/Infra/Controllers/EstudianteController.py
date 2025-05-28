from flask import request, jsonify
from ..Models.EstudianteModels import db, Estudiantes
from datetime import datetime
from .Errors import ErrorClient as errorCliente
import bcrypt
from sqlalchemy.exc import IntegrityError

# Obtener todos los estudiantes
def getEstudiantes():
    estudiantes = Estudiantes.query.all()
    if estudiantes is None:
        raise errorCliente.NotFoundError(description="No existen estudiantes registrados")
    return jsonify([s.to_dict() for s in estudiantes]), 200

# Obtener un solo estudiante por ID
def getEstudiante(id):
    estudiante = Estudiantes.query.get(id)
    if estudiante is None:
        raise errorCliente.NotFoundError(description="Estudiante no encontrado")
    return jsonify(estudiante.to_dict()), 200

# Crear estudiante
def crearEstudiante():
    data = request.get_json()

    required_fields = ["nombre_estudiante", "apellido_estudiante", "correo_estudiante", "contrasenia",
                       "fecha_nacimiento", "numero_celular", "id_pais", "id_ciudad"]

    if not all(field in data for field in required_fields):
        raise errorCliente.BadRequest(description="Faltan campos obligatorios")
    
    # Hashear la contraseña antes de guardar
    contrasenia_hash = bcrypt.hashpw(data["contrasenia"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


    estudiante = Estudiantes(
        nombre_estudiante = data["nombre_estudiante"],
        apellido_estudiante = data["apellido_estudiante"],
        correo_estudiante = data["correo_estudiante"],
        contrasenia = contrasenia_hash,
        fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%Y-%m-%d"),
        fecha_registro = datetime.now(),
        numero_celular = data["numero_celular"],
        id_pais = data["id_pais"],
        id_ciudad = data["id_ciudad"]
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

# Actualizar estudiante perfil
def actulizarEstudiante(id_estudiante):
    estudiante = Estudiantes.query.get(id_estudiante)
    if not estudiante:
        raise errorCliente.NotFoundError(description = "Estudiante no encontrado")

    data = request.get_json()

    # Se actualizan solo los campos presentes
    estudiante.nombre_estudiante = data.get("nombre_estudiante", estudiante.nombre_estudiante)
    estudiante.apellido_estudiante = data.get("apellido_estudiante", estudiante.apellido_estudiante)
    estudiante.correo_estudiante = data.get("correo_estudiante", estudiante.correo_estudiante)
    estudiante.fecha_nacimiento = data.get("fecha_nacimiento", estudiante.fecha_nacimiento)
    estudiante.numero_celular = data.get("numero_celular", estudiante.numero_celular)
    estudiante.id_pais = data.get("id_pais", estudiante.id_pais)
    estudiante.id_ciudad = data.get("id_ciudad", estudiante.id_ciudad)

    db.session.commit()
    return jsonify({"status": 200, 
                    "message": "Estudiante actualizado correctamente",
                    "data": estudiante.to_dict()}), 200


# Eliminar un estudiante
def eleminarEstudiante(id):
    estudiante = Estudiantes.query.get(id)
    if not estudiante:
        raise errorCliente.NotFoundError(description = "Estudiante no encontrado")

    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({"status": 200,
                    "message": "Estudiante eliminado correctamente"}),200