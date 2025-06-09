import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Main import app

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente

def test_getPaises(cliente):
    respuesta = cliente.get("/api/paises")
       
    assert respuesta.json["status"] == 200
    assert respuesta.json["message"] == "Lista de paises"
    assert isinstance(respuesta.json["data"], list)

    assert len(respuesta.json["data"]) > 0

    assert isinstance(respuesta.json["data"][0], dict)
    assert "id_pais" in respuesta.json["data"][0]
    assert "nombre_pais" in respuesta.json["data"][0]

def test_getCiudades(cliente):
    respuesta = cliente.get("/api/ciudades/1")
       
    assert respuesta.json["status"] == 200
    assert respuesta.json["message"] == "Lista de ciudades del pais"
    assert isinstance(respuesta.json["data"], list)

    assert len(respuesta.json["data"]) > 0
    assert isinstance(respuesta.json["data"][0], dict)
    assert "id_ciudad" in respuesta.json["data"][0]
    assert "nombre_ciudad" in respuesta.json["data"][0]