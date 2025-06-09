import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Main import app

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente

def test_loginExitoso(cliente):
    datos = { "correo_estudiante": "juanPerez@gmail.com",
              "contrasenia": "abc123"
            }
    response = cliente.post("/api/login/", json=datos)
    assert response.json["status"] == 200
    assert response.json["message"] == "Login exitoso"

def test_loginContatraseniaInvalida(cliente):
    datos = { "correo_estudiante": "juanPerez@gmail.com",
               "contrasenia": "hola123"
            }
    response = cliente.post("/api/login/", json=datos)
    assert response.json["status"] == 401
    assert response.json["message"] ==  "Credenciales inválidas"

def test_loginCorreoInvalido(cliente):
    datos = {"correo_estudiante": "noexiste@example.com", 
             "contrasenia": "123456"
            }
    response = cliente.post("/api/login/", json=datos)
    assert response.json["status"] == 401
    assert response.json["message"] ==  "Credenciales inválidas"

def test_loginCamposFaltantes(cliente):
    response = cliente.post("/api/login/", json={})
    assert response.json["status"] == 400
    assert response.json["message"] == "Correo y contraseña son obligatorios"
    

    