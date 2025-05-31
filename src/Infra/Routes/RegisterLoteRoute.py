from flask import Blueprint
from Infra.Controllers import RegisterLoteController

# Crear un Blueprint para agrupar rutas del recurso estudiante
registrarLote = Blueprint('registrarLoteEstudiantes', __name__)

@registrarLote.route("/", methods=["POST"])
def registrarLoteEstudiantes():
    return RegisterLoteController.registrarLoteEstudiantes()