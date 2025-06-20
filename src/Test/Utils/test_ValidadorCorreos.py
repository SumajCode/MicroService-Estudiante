from Infra.Utils.ValidadorCorreosUtils import validarDominioInstitucional
from Main import app
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

@pytest.fixture
def cliente():
    with app.test_client() as cliente:
        yield cliente

def test_validarDominioInstitucional():
    assert validarDominioInstitucional("201705944@est.umss.edu") == True
    assert validarDominioInstitucional("201705944@est.ums.edu") == False