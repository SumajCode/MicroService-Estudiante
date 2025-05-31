from flask import Blueprint
from Infra.Controllers import LoginController

# Crear un Blueprint para agrupar rutas del recurso estudiante
login = Blueprint('login', __name__)

@login.route("/", methods=["POST"])
def loginEstudiante():
    return LoginController.loginEstudiante()

@login.route("/cambiarContrasenia", methods=["PUT"])
#@jwt_required()  # o el sistema que uses
def cambiarContrasenia():
    return LoginController.cambiarContrasenia()