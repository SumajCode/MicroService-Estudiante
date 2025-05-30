from flask import request, jsonify
from ..Models.EstudianteModels import db, Estudiantes
from datetime import datetime
from .Errors import ErrorClient as errorCliente
from .Errors import ErrorServer as errorServer
import bcrypt
from sqlalchemy.exc import IntegrityError

# Obtener todos los estudiantes
def getEstudiantes():
    estudiantes = Estudiantes.query.all()
    if not estudiantes:
        raise errorCliente.NotFoundError(description="No existen estudiantes registrados")
    try:
        return jsonify({"status": 200,
                        "message": "Lista de estudiantes",
                        "data": [filtrarContrasenia(s.to_dict()) for s in estudiantes]}), 200
    except Exception as e:
        raise errorServer.serverError(description=str(e))
    
# Obtener un solo estudiante por ID
def getEstudiante(id):
    estudiante = Estudiantes.query.get(id)
    if not estudiante:
        raise errorCliente.NotFoundError(description="Estudiante no encontrado")
    try: 
        estudianteFiltrado = filtrarContrasenia(estudiante.to_dict())
        return jsonify({"status": 200,
                        "message": "Informacion del estudiante",
                        "data":estudianteFiltrado}), 200
    except: 
        raise errorServer.serverError(description="Error al obtener el estudiante")
    
def filtrarContrasenia(estudianteDict):
    estudianteDict.pop('contrasenia', None)
    return estudianteDict

# Crear estudiante
def crearEstudiante():
    data = request.get_json()
    required_fields = ["nombre_estudiante", "apellido_estudiante", "correo_estudiante", "contrasenia",
                       "fecha_nacimiento", "numero_celular", "id_pais", "id_ciudad"]

    if not all(field in data for field in required_fields):
        raise errorCliente.BadRequest(description="Todos los campos son obligatorios")
    
    # Hashear la contraseña antes de guardar
    contrasenia_hash = bcrypt.hashpw(data["contrasenia"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    estudiante = Estudiantes(
        nombre_estudiante = data["nombre_estudiante"],
        apellido_estudiante = data["apellido_estudiante"],
        correo_estudiante = data["correo_estudiante"],
        contrasenia = contrasenia_hash,
        fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%d-%m-%Y"),
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

def crearEstudianteLista():
    data = request.get_json()
    required_fields = ["nombre_estudiante", "apellido_estudiante", "correo_estudiante", "contrasenia",
                       "fecha_nacimiento", "numero_celular", "id_pais", "id_ciudad"]

    if not all(field in data for field in required_fields):
        raise errorCliente.BadRequest(description="Todos los campos son obligatorios")
    
    # Hashear la contraseña antes de guardar
    contrasenia_hash = bcrypt.hashpw(data["contrasenia"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    estudiante = Estudiantes(
        nombre_estudiante = data["nombre_estudiante"],
        apellido_estudiante = data["apellido_estudiante"],
        correo_estudiante = data["correo_estudiante"],
        contrasenia = contrasenia_hash,
        fecha_nacimiento = datetime.strptime(data["fecha_nacimiento"], "%d-%m-%Y"),
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
def actulizarEstudiante(idEstudiante):
    estudiante = Estudiantes.query.get(idEstudiante)
    if not estudiante:
        raise errorCliente.NotFoundError(description = "Estudiante no encontrado")

    data = request.get_json()
    camposActualizables = ['nombre_estudiante', 'apellido_estudiante', 'fecha_nacimiento',
                           'numero_celular', 'id_pais', 'id_ciudad']

    for campo in camposActualizables:
        if campo in data:
            setattr(estudiante, campo, data[campo])
    try:
        db.session.commit()
        return jsonify({"status": 200, 
                        "message": "Estudiante actualizado correctamente",
                        "data": filtrarContrasenia(estudiante.to_dict())}), 200
    except IntegrityError as e:
        raise errorServer.serverError(description=str(e))

# Eliminar un estudiante
def eleminarEstudiante(id):
    estudiante = Estudiantes.query.get(id)
    if not estudiante:
        raise errorCliente.NotFoundError(description = "Estudiante no encontrado")
    try:
        db.session.delete(estudiante)
        db.session.commit()
        return jsonify({"status": 200,
                        "message": "Estudiante eliminado correctamente"}),200
    except Exception as e:
        raise errorServer.serverError(description=str(e))