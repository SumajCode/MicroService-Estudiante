from flask import Blueprint
from Infra.Controllers import PaisCiudadController

# Crear un Blueprint para agrupar rutas del recurso pais
paisCiudad = Blueprint('paisCiudad', __name__)

@paisCiudad.route('/paises', methods=['GET'])
def obtenerTodoPaises():
    return PaisCiudadController.obtenerPaises()

@paisCiudad.route("/ciudades/<int:id>", methods=["GET"])
def obtenerTodoCiudades(id):
    return PaisCiudadController.obtenerCiudades(id)