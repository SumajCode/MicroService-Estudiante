import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Main import app 

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente


# Obtener todos los estudiantes
def test_getEstudiantes(cliente):
    respuesta = cliente.get("/api/estudiantes/")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json, list)

# Obtener un estudiante por ID (si existe)
def test_getEstudianteID(cliente):
    respuesta = cliente.get("/api/estudiantes/1")
    if respuesta.status_code == 404:
        assert respuesta.json["message"] == "Estudiante no encontrado"
    else:
        assert respuesta.status_code == 200
        assert "nombre_estudiante" in respuesta.json

# Crear un estudiante y guardar el ID para las siguientes pruebas
def test_crearEstudiante(cliente):
    datos = {
        "nombre_estudiante": "Pedro Eliminar",
        "apellido_estudiante": "López",
        "correo_estudiante": "pedros@example.com",
        "contrasenia": "123456",
        "fecha_nacimiento": "2000-01-01",
        "numero_celular": "78945612",
        "id_pais": 1,
        "id_ciudad": 1
    }
    respuesta = cliente.post("/api/estudiantes/registrar", json=datos)
    assert respuesta.status_code == 201
    json = respuesta.json
    assert json["correo_estudiante"] == datos["correo_estudiante"]

    # Guardar el ID para usar en las siguientes pruebas
    global ultimo_estudiante_id
    ultimo_estudiante_id = json["id_estudiante"]  # Ajusta al nombre correcto de tu campo ID


# Actualizar el último estudiante creado
def test_actualizarEstudiante(cliente):
    datos_actualizados = {
        "nombre_estudiante": "Pedro Actualizado"
    }

    respuesta = cliente.put(f"/api/estudiantes/actualizar/{ultimo_estudiante_id}", json=datos_actualizados)
    if respuesta.status_code == 404:
        assert respuesta.json["message"] == "Estudiante no encontrado"
    else:
        assert respuesta.status_code == 200
        assert respuesta.json["nombre_estudiante"] == "Pedro Actualizado"


# Eliminar el último estudiante creado
def test_eliminarEstudiante(cliente):
    respuesta = cliente.delete(f"/api/estudiantes/eleminar/{ultimo_estudiante_id}")
    assert respuesta.status_code in [200, 404]
    if respuesta.status_code == 200:
        assert respuesta.json["message"] == "Estudiante eliminado correctamente"
    else:
        assert respuesta.json["message"] == "Estudiante no encontrado"

