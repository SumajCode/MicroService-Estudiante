from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address  
from Infra.Controllers import EstudianteController

# Crear un Blueprint para agrupar rutas del recurso estudiante
estudiante = Blueprint('estudiantes', __name__)
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per day"])

# Definir rutas CRUD
@estudiante.route("/", methods=["GET"])
def getEstudiantes():
    return EstudianteController.getEstudiantes()

@estudiante.route("/<int:id>", methods=["GET"])
def getEstudiante(id):
    return EstudianteController.getEstudiante(id)

@estudiante.route("/registrar", methods=["POST"])
@limiter.limit("2 per minute")  # Limita 5 registros por IP cada minuto
def crearEstudiante():
    return EstudianteController.crearEstudiante()

#estudiante.route("/registrarLista", methods=["POST"])
#def crearEstudianteLista():
#    return EstudianteController.crearEstudianteLista()

@estudiante.route("/actualizar/<int:id_estudiante>", methods=["PUT"])
def actulizarEstudiante(id_estudiante):
    return EstudianteController.actulizarEstudiante(id_estudiante)

@estudiante.route("/eleminar/<int:id>", methods=["DELETE"])
def eleminarEstudiante(id):
    return EstudianteController.eleminarEstudiante(id)


