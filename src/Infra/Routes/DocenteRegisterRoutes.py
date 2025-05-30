from flask import Blueprint
from Infra.Controllers import DocenteRegisterController

# Crear un Blueprint para agrupar rutas del recurso estudiante
registrarEstudiantesDocente = Blueprint('registrorEstudiantesDocente', __name__)

@registrarEstudiantesDocente.route("/", methods=["POST"])
def registrarEstudiantesDocente():
    return DocenteRegisterController.registrarEstudiantesDocente()