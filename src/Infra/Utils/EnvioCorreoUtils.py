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
        raise errorCliente.BadRequest(description="Ingrese un correo valido") 
    
    mensaje_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #306998;
            color: white;
            padding: 15px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            padding: 20px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }}
        .credentials {{
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .password {{
            font-family: monospace;
            color: #306998;
            font-weight: bold;
            margin-right: 10px;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h2>PythonLab - Plataforma de Aprendizaje</h2>
    </div>
    
    <div class="content">
        <p>¡Bienvenido/a a <strong>PythonLab</strong>! Estamos encantados de tenerte como parte de nuestra comunidad de aprendizaje.</p>
        
        <div class="credentials">
            <h3>Credenciales de acceso</h3>
            <p><strong>Correo electrónico:</strong> {destinatario}</p>
            <p><strong>Contraseña:</strong> <span class="password">{contrasenia}</span>
        </div>
        
        <p>Por seguridad, te recomendamos:</p>
        <ul>
            <li>Cambiar esta contraseña temporal al iniciar sesión</li>
            <li>No compartir tus credenciales con nadie</li>
            <li>Usar una contraseña segura y única</li>
        </ul>
        
        <div class="footer">
            <p>Este correo fue generado automáticamente. Por favor no respondas a este mensaje.</p>
            <p>© 2025 PythonLab. Todos los derechos reservados.</p>
        </div>
    </div>
</body>
</html>
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