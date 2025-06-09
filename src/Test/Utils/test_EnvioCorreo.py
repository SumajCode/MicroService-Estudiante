from Infra.Utils.EnvioCorreoUtils import enviarCorreoEstudiante
from Infra.Controllers.Errors import ErrorClient, ErrorServer
from Main import app
from unittest.mock import patch
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente

def test_enviarCorreoEstudianteExitoso():
    with app.app_context():
        response = enviarCorreoEstudiante("201705944@est.umss.edu", "AsdRdsF1")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["message"] == "Correo enviado exitosamente"


def test_enviarCorreoEstudianteCorreoObligatorio():
    with app.app_context():
        with pytest.raises(ErrorClient.BadRequest) as exc_info:
            enviarCorreoEstudiante(None, "clave123")
        assert exc_info.value.description == "Ingrese un correo valido"

@patch("Infra.Utils.EnvioCorreoUtils.enviarCorreo", return_value=False)
def test_enviarCorreoEstudianteError(mock_enviar):
    with app.app_context():
        with pytest.raises(ErrorServer.serverError) as exc_info:
            enviarCorreoEstudiante("201705944@est.umss.edu", "clave123")
        assert exc_info.value.description == "Error al enviar el correo"
        assert mock_enviar.called



