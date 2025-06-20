import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Main import app

ultimo_estudiante_id = None

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente

def test_getEstudiantes(cliente):
    respuesta = cliente.get("/api/estudiantes/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json, dict)
    assert "status" in respuesta.json
    assert "message" in respuesta.json
    assert "data" in respuesta.json

    assert respuesta.json["status"] == 200
    assert respuesta.json["message"] == "Lista de estudiantes"
    assert isinstance(respuesta.json["data"], list)

def test_getEstudianteID(cliente):
    respuesta = cliente.get("/api/estudiantes/2")
    
    if respuesta.status_code == 404:
        assert respuesta.json["message"] == "Estudiante no encontrado"
    else:
        assert respuesta.status_code == 200
        assert "data" in respuesta.json
        assert respuesta.json["message"] == "Informacion del estudiante"
        assert "nombre_estudiante" in respuesta.json["data"]
        assert isinstance(respuesta.json["data"], dict)

def test_crearEstudiante(cliente):
    global ultimo_estudiante_id

    datos = {
        "nombre_estudiante": "Pedro Eliminar",
        "apellido_estudiante": "López",
        "correo_estudiante": "pedros@example.com",
        "contrasenia": "123456",
        "fecha_nacimiento": "01-01-2000",
        "numero_celular": "78945612",
        "id_pais": 1,
        "id_ciudad": 1
    }

    respuesta = cliente.post("/api/estudiantes/registrar", json=datos)
    assert respuesta.status_code == 201
    assert respuesta.json["status"] == 201
    assert respuesta.json["message"] == "Estudiante creado exitosamente"
    assert respuesta.json["data"]["correo_estudiante"] == datos["correo_estudiante"]

    ultimo_estudiante_id = respuesta.json["data"]["id_estudiante"]

def test_actualizarEstudiante(cliente):
    global ultimo_estudiante_id

    datosActualizados = {
        "nombre_estudiante": "Pedro Actualizado"
    }

    respuesta = cliente.put(f"/api/estudiantes/actualizar/{ultimo_estudiante_id}", json=datosActualizados)
    if respuesta.status_code == 404:
        assert respuesta.json["message"] == "Estudiante no encontrado"
    else:
        assert respuesta.json["status"] == 200
        assert respuesta.json["data"]["nombre_estudiante"] == "Pedro Actualizado"
        assert respuesta.json["message"] == "Estudiante actualizado correctamente"

def test_eliminarEstudiante(cliente):
    global ultimo_estudiante_id

    respuesta = cliente.delete(f"/api/estudiantes/eleminar/{ultimo_estudiante_id}")
    assert respuesta.status_code in [200, 404]
    if respuesta.status_code == 200:
        assert respuesta.json["status"] == 200
        assert respuesta.json["message"] == "Estudiante eliminado correctamente"
    else:
        assert respuesta.json["status"] == 404
        assert respuesta.json["message"] == "Estudiante no encontrado"
