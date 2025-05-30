from flask import request, jsonify
from ..Models.EstudianteModels import db, Estudiantes
from .Errors import ErrorClient as errorCliente
from .Errors import ErrorServer as errorServer
from email.mime.multipart import MIMEMultipart
from sqlalchemy.exc import IntegrityError
from email.mime.text import MIMEText
import random, string, bcrypt, smtplib
from Config.Config import Config
from datetime import datetime

def crearCuentaEstudianteDocente():
    data = request.get_json()
    required_fields = ["correo_estudiante", "nombre_estudiante", "apellido_estudiante"] 

    if not all(field in data for field in required_fields):
        raise errorCliente.BadRequest(description="Todos los campos son obligatorios")

    contrasenia = generarContrasenia()
    contrasenia_hash = bcrypt.hashpw(contrasenia.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    estudiante = Estudiantes(
        nombre_estudiante = data["nombre_estudiante"],
        apellido_estudiante = data["apellido_estudiante"],
        correo_estudiante = data["correo_estudiante"],
        contrasenia = contrasenia_hash,
        fecha_registro = datetime.now(),
        es_universitario = validarDominioInstitucional(data["correo_estudiante"]),
        id_pais = 1,    # Bolivia
        id_ciudad = 3   # Cochabamba
    )
    try:
        db.session.add(estudiante)
        db.session.flush()  # Inserta en la base sin hacer commit aún

        enviarCorreoEstudiante(data["correo_estudiante"], contrasenia)
        db.session.commit()  # Solo se hace si todo fue exitoso
        return jsonify({
            "status": 201,
            "message": "Estudiante registrado exitosamente",
            "data": estudiante.to_dict()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        mensaje_bd = str(e.orig)
        if "unique constraint" in mensaje_bd.lower() or "duplicate" in mensaje_bd.lower():
            raise errorCliente.BadRequest(description="Ya existe un usuario con ese correo.")
        else:
            raise errorCliente.BadRequest(description=f"Error en la base de datos: {mensaje_bd}")
    except Exception as e:
        db.session.rollback()
        raise errorServer.serverError(description="Error al crear la cuenta, por favor intente nuevamente.")


def enviarCorreoEstudiante(correoEstudiante, contrasenia):
    destinatario = correoEstudiante

    if not destinatario:
        raise errorCliente.BadRequest(description="Correo requerido") 
    
    mensaje_html = f"""
    <h2>PythonLab - Plataforma de Aprendizaje</h2>
    <p>Gracias por crear una cuenta en <strong>PythonLab</strong>. Estamos encantados de tenerte como parte de nuestra comunidad.</p>
    <p><strong>Credenciales de usuario:</p>
    <p><strong>Correo electrónico:</strong> {destinatario}</p>
    <p><strong>Contraseña temporal:</strong> <span style="color:blue;">{contrasenia}</span></p>
    <p>Te recomendamos cambiar tu contraseña una vez hayas iniciado sesión.</p>
    """
    if enviarCorreo(destinatario, "Creacion de cuenta en PythonLab", mensaje_html):
        return jsonify({"status": 200, "message": "Correo enviado exitosamente"})
    else:
        raise errorServer.serverError(description="Error al enviar el correo")

def enviarCorreo(destinatario, asunto, mensaje_html):
    try:
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_REMITENTE
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(mensaje_html, 'html'))

        # Conexión SMTP segura con Gmail
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(Config.EMAIL_REMITENTE, Config.EMAIL_PASSWORD)
        servidor.send_message(msg)
        servidor.quit()

        print("Correo enviado correctamente.")
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

def generarContrasenia(longitud=8):
    caracteres = string.ascii_letters  # Solo letras (A-Z, a-z)
    return ''.join(random.choices(caracteres, k=longitud))

def validarDominioInstitucional(correo):
    dominiosValidos = ["est.umss.edu", "umss.edu.bo"]
    return any(correo.lower().endswith(f"@{dominio}") for dominio in dominiosValidos)

