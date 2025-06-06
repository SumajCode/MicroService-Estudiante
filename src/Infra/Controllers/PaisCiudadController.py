from flask import request, jsonify
from ..Models.EstudianteModels import Ciudad, Pais
from .Errors import ErrorClient as errorCliente
from .Errors import ErrorServer as errorServer

def obtenerPaises():
    paises = Pais.query.all()
    if not paises:
        raise errorCliente.NotFoundError(description="No existen paises registrados")
    try:
        return jsonify({"status": 200,
                        "message": "Lista de paises",
                        "data": [pais.to_dict() for pais in paises]}), 200
    except Exception as e:
        raise errorServer.serverError(description=str(e))

def obtenerCiudades(idPais):
    ciudades = Ciudad.query.filter_by(id_pais=idPais).all()
    if not ciudades:
        raise errorCliente.NotFoundError(description="No existen ciudades registrados")
    try:
        return jsonify({"status": 200,
                        "message": "Lista de ciudades del pais",
                         "data": [ciudad.to_dict() for ciudad in ciudades]}), 200
    except Exception as e:
        raise errorServer.serverError(description=str(e))