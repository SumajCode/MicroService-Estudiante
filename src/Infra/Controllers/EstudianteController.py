from flask import request, jsonify
from ..Models.EstudianteModels import db, Estudiantes
from datetime import datetime


# Obtener todos los estudiantes
def getEstudiantes():
    estudiantes = Estudiantes.query.all()
    return jsonify([s.to_dict() for s in estudiantes])

# Obtener un solo estudiante por ID
def getEstudiante(id):
    estudiante = Estudiantes.query.get(id)
    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404
    return jsonify(estudiante.to_dict())

# Crear estudiante
def crearEstudiante():
    data = request.get_json()

    required_fields = ["nombre_estudiante", "apellido_estudiante", "correo_estudiante", "contrasenia",
                       "fecha_nacimiento", "numero_celular", "id_pais", "id_ciudad"]

    if not all(field in data for field in required_fields):
        return jsonify({"message": "Faltan campos obligatorios"}), 400

    estudiante = Estudiantes(
        nombre_estudiante = data["nombre_estudiante"],
        apellido_estudiante = data["apellido_estudiante"],
        correo_estudiante = data["correo_estudiante"],
        contrasenia = data["contrasenia"],
        fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%Y-%m-%d"),
        fecha_registro = datetime.now(),
        numero_celular = data["numero_celular"],
        id_pais = data["id_pais"],
        id_ciudad = data["id_ciudad"]
    )

    db.session.add(estudiante)
    db.session.commit()
    return jsonify(estudiante.to_dict()), 201

# Actualizar estudiante
def actulizarEstudiante(id_estudiante):
    estudiante = Estudiantes.query.get(id_estudiante)
    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404

    data = request.get_json()

    # Se actualizan solo los campos presentes
    estudiante.nombre_estudiante = data.get("nombre_estudiante", estudiante.nombre_estudiante)
    estudiante.apellido_estudiante = data.get("apellido_estudiante", estudiante.apellido_estudiante)
    estudiante.correo_estudiante = data.get("correo_estudiante", estudiante.correo_estudiante)
    estudiante.contrasenia = data.get("contrasenia", estudiante.contrasenia)
    estudiante.fecha_nacimiento = data.get("fecha_nacimiento", estudiante.fecha_nacimiento)
    estudiante.numero_celular = data.get("numero_celular", estudiante.numero_celular)
    estudiante.id_pais = data.get("id_pais", estudiante.id_pais)
    estudiante.id_ciudad = data.get("id_ciudad", estudiante.id_ciudad)

    db.session.commit()
    return jsonify(estudiante.to_dict())


# Eliminar un estudiante
def eleminarEstudiante(id):
    estudiante = Estudiantes.query.get(id)
    if not estudiante:
        return jsonify({"message": "Estudiante no encontrado"}), 404

    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({"message": "Estudiante eliminado correctamente"})