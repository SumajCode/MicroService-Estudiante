from flask import request, jsonify
from ..Utils.GenerarContraseniaUtils import filtrarContrasenia, generarContrasenia
from ..Utils.ValidadorCorreosUtils import validarDominioInstitucional
from ..Models.EstudianteModels import db, Estudiantes
from ..Utils.EnvioCorreoUtils import enviarCorreoEstudiante
from .Errors import ErrorClient as errorCliente
from .Errors import ErrorServer as errorServer
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import bcrypt

def registrarLoteEstudiantes():
    lista_estudiantes = request.get_json()
    resultados = registrarEstudiantes(lista_estudiantes)
    return jsonify({
        "status": 207,
        "message": "Resultado del registro por lote",
        "resultados": resultados
    }), 207

def registrarEstudiantes(lista_estudiantes):
    resultados = []

    if not isinstance(lista_estudiantes, list):
        raise errorCliente.BadRequest(description="Se esperaba una lista de estudiantes.")

    for data in lista_estudiantes:
        required_fields = ["correo_estudiante", "nombre_estudiante", "apellido_estudiante"]
        if not all(field in data for field in required_fields):
            resultados.append({
                "correo_estudiante": data.get("correo_estudiante", "correo no especificado"),
                "status": 400,
                "message": "Todos los campos son obligatorios"
            })
            continue

        contrasenia = generarContrasenia()
        contrasenia_hash = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        estudiante = Estudiantes(
            nombre_estudiante=data["nombre_estudiante"],
            apellido_estudiante=data["apellido_estudiante"],
            correo_estudiante=data["correo_estudiante"],
            contrasenia=contrasenia_hash,
            fecha_registro=datetime.now(),
            es_universitario=validarDominioInstitucional(data["correo_estudiante"]),
            id_pais=1,
            id_ciudad=3
        )

        try:
            db.session.add(estudiante)
            db.session.flush()  # inserta sin commitear aún
            enviarCorreoEstudiante(data["correo_estudiante"], contrasenia)
            db.session.commit()
            estudianteFiltrado = filtrarContrasenia(estudiante.to_dict())
            resultados.append({
                "correo_estudiante": data["correo_estudiante"],
                "status": 201,
                "message": "Estudiante registrado exitosamente",
                "data": estudianteFiltrado
            })
        except IntegrityError as e:
            db.session.rollback()
            mensaje_bd = str(e.orig)
            resultados.append({
                "correo_estudiante": data["correo_estudiante"],
                "status": 400,
                "message": "Ya existe un usuario con ese correo." if "unique constraint" in mensaje_bd.lower() or "duplicate" in mensaje_bd.lower()
                           else f"Error en la base de datos: {mensaje_bd}"
            })
        except Exception as e:
            db.session.rollback()
            resultados.append({
                "correo_estudiante": data["correo_estudiante"],
                "status": 500,
                "message": "Error al crear la cuenta, por favor intente nuevamente."
            })

    return resultados

