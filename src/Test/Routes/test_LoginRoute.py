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
              "contrasenia":"abcdefghij"
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
             "contrasenia": "abcdefghij"
            }
    response = cliente.post("/api/login/", json=datos)
    assert response.json["status"] == 401
    assert response.json["message"] ==  "Credenciales inválidas"

def test_loginCamposFaltantes(cliente):
    response = cliente.post("/api/login/", json={})
    assert response.json["status"] == 400
    assert response.json["message"] == "Correo y contraseña son obligatorios"
    
def test_cambiarContraseniaExitoso(cliente):
    datos = { "correo_estudiante": "juanPerez@gmail.com",
              "contrasenia_actual": "abcdefghij",
              "nueva_contrasenia": "abcdefghij"
            }
    response = cliente.put("/api/login/cambiarContrasenia", json=datos)
    assert response.json["status"] == 200
    assert response.json["message"] == "Contraseña cambiada exitosamente"

def test_cambiarContraseniaConContraseniaInvalida(cliente):
    datos = { "correo_estudiante": "juanPerez@gmail.com",
              "contrasenia_actual": "abcdefghijs",
              "nueva_contrasenia": "abcdefghij"
            }
    response = cliente.put("/api/login/cambiarContrasenia", json=datos)
    assert response.json["status"] == 401
    assert response.json["message"] == "La contraseña actual es incorrecta"

def test_cambiarContraseniaConNuevaContraseniaInvalida(cliente):
    datos = { "correo_estudiante": "juanPerez@gmail.com",
              "contrasenia_actual": "abcdefghij",
              "nueva_contrasenia": "abcde"
            }
    response = cliente.put("/api/login/cambiarContrasenia", json=datos)
    assert response.json["status"] == 400
    assert response.json["message"] == "La nueva contraseña debe tener al menos 8 caracteres"

def test_cambiarContraseniaEstudianteNoEncontrado(cliente):
    datos = { "correo_estudiante": "juanPerezA@gmail.com",
              "contrasenia_actual": "abcdefghij",
              "nueva_contrasenia": "abcdefghij"
            }
    
    response = cliente.put("/api/login/cambiarContrasenia", json=datos)
    assert response.json["status"] == 404
    assert response.json["message"] == "Estudiante no encontrado"

def test_cambiarContraseniaEviarContraseniaNuevaActual(cliente):
    datos = { "correo_estudiante": "juanPerezA@gmail.com"}
    
    response = cliente.put("/api/login/cambiarContrasenia", json=datos)
    assert response.json["status"] == 400
    assert response.json["message"] == "Debe enviar la contraseña actual y la nueva contraseña"