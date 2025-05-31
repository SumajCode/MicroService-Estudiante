from flask import request, jsonify
from ..Models.EstudianteModels import db, Estudiantes
from .Errors import ErrorClient as errorCliente
from .Errors import ErrorServer as errorServer
import bcrypt

def loginEstudiante():
    try:
        data = request.get_json()
        email = data.get("correo_estudiante")
        password = data.get("contrasenia")

        if not email or not password:
            raise errorCliente.BadRequest(description="Correo y contraseña son obligatorios")

        estudiante = Estudiantes.query.filter_by(correo_estudiante=email).first()
        if not estudiante:
            raise errorCliente.InvalidUser(description="Credenciales inválidas")
        if not bcrypt.checkpw(password.encode('utf-8'), estudiante.contrasenia.encode('utf-8')):
            raise errorCliente.InvalidUser(description="Credenciales inválidas")

        return jsonify({
            "status": 200,
            "message": "Login exitoso",
            "data": {
                "id_estudiante": estudiante.id_estudiante,
                "nombre_estudiante": estudiante.nombre_estudiante,
                "correo_estudiante": estudiante.correo_estudiante
            }
        }), 200
    except (errorCliente.BadRequest, errorCliente.InvalidUser):
        raise
    except Exception as e:
        raise errorServer.serverError(description="Error interno en el servidor")

def cambiarContrasenia():
    try:
        data = request.get_json()
        correo = data.get("correo_estudiante")
        contraseniaActual = data.get("contrasenia_actual")
        nuevaContrasenia = data.get("nueva_contrasenia")

        if not contraseniaActual or not nuevaContrasenia:
            raise errorCliente.BadRequest(description="Debe enviar la contraseña actual y la nueva contraseña")

        estudiante = Estudiantes.query.filter_by(correo_estudiante=correo).first()

        if not estudiante:
            raise errorCliente.NotFoundError(description="Estudiante no encontrado")
        
        if not bcrypt.checkpw(contraseniaActual.encode('utf-8'), estudiante.contrasenia.encode('utf-8')):
            raise errorCliente.InvalidUser(description="La contraseña actual es incorrecta") 
 
        if len(nuevaContrasenia) < 8:
            raise errorCliente.BadRequest(description="La nueva contraseña debe tener al menos 8 caracteres")

        estudiante.contrasenia = bcrypt.hashpw(nuevaContrasenia.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.session.commit()

        return jsonify({
            "status": 200,
            "message": "Contraseña cambiada exitosamente"
        }), 200

    except (errorCliente.BadRequest, errorCliente.InvalidUser, errorCliente.NotFoundError):
        raise
    except Exception as e:
        db.session.rollback()
        raise errorServer.serverError(description=str(e))
