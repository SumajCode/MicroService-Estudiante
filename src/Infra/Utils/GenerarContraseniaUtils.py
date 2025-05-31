import random, string

def generarContrasenia(longitud=8):
    caracteres = string.ascii_letters  # Solo letras (A-Z, a-z)
    return ''.join(random.choices(caracteres, k=longitud))

def filtrarContrasenia(estudianteDict):
    estudianteDict.pop('contrasenia', None)
    return estudianteDict