from flask import Blueprint
from Infra.Controllers import EstudianteController

# Crear un Blueprint para agrupar rutas del recurso estudiante
estudiante = Blueprint('estudiantes', __name__)

# Definir rutas CRUD
@estudiante.route("/", methods=["GET"])
def getEstudiantes():
    return EstudianteController.getEstudiantes()

@estudiante.route("/<int:id>", methods=["GET"])
def getEstudiante(id):
    return EstudianteController.getEstudiante(id)

@estudiante.route("/registrar", methods=["POST"])
def crearEstudiante():
    return EstudianteController.crearEstudiante()

@estudiante.route("/actualizar/<int:id_estudiante>", methods=["PUT"])
def actulizarEstudiante(id_estudiante):
    return EstudianteController.actulizarEstudiante(id_estudiante)

@estudiante.route("/eleminar/<int:id>", methods=["DELETE"])
def eleminarEstudiante(id):
    return EstudianteController.eleminarEstudiante(id)


