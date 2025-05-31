from flask import jsonify
from ..Controllers.Errors import ErrorClient as errorCliente
from ..Controllers.Errors import ErrorServer as errorServer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Config.Config import Config
import smtplib


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