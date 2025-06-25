from flask import Blueprint, request
from Infra.Controllers import LoginController

# Crear un Blueprint para agrupar rutas del recurso estudiante
login = Blueprint('login', __name__)

@login.route("/", methods=["POST", "OPTIONS"])
def loginEstudiante():
    if request.method == "OPTIONS":
        return "", 200 
    return LoginController.loginEstudiante()

@login.route("/cambiarContrasenia", methods=["PUT"])
#@jwt_required()  # o el sistema que uses
def cambiarContrasenia():
    return LoginController.cambiarContrasenia()