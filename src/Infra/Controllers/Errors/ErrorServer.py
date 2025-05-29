from werkzeug.exceptions import HTTPException

class serverError(HTTPException):
    code = 500
    description = 'Error interno del servidor.'