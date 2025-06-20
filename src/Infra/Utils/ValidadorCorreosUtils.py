import re

def validarDominioInstitucional(correo):
    dominiosValidos = [
        "est.umss.edu", 
        "est.umss.edu.bo"
    ]
    patron = r'^\d+@(?:' + '|'.join(map(re.escape, dominiosValidos)) + ')$'
    return bool(re.fullmatch(patron, correo))