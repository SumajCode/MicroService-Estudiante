from Infra.Utils.GenerarContraseniaUtils import generarContrasenia, filtrarContrasenia
from Main import app
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente

def test_generarContrasenia():
    contrasenia = generarContrasenia()
    assert len(contrasenia) == 8
    assert contrasenia.isalpha()

def test_generarContraseniaPersonalizada():
    contrasenia = generarContrasenia(12)
    assert len(contrasenia) == 12
    assert contrasenia.isalpha()

def test_filtrarContrasenia():
    datos = {
        "nombre": "Juan",
        "contrasenia": "secreta123",
        "correo": "juan@mail.com"
    }
    resultado = filtrarContrasenia(datos.copy())
    assert "contrasenia" not in resultado
    assert resultado["nombre"] == "Juan"
    assert resultado["correo"] == "juan@mail.com"
