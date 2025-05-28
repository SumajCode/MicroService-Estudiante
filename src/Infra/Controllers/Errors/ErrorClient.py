from werkzeug.exceptions import HTTPException

class invalidAccess(HTTPException):
    code = 403
    description = 'Acceso del usuario no autorizado al sistema.'

class NotFoundError(HTTPException):
    code = 404
    description = 'Recurso solicitado no encontrado.'

class InvalidUser(HTTPException):
    code = 401
    description = 'Autenticación del usuario necesaria.'

class BadRequest(HTTPException):
    code = 400
    description = 'Solicitud incorrecta.'

class methodNotAllowed(HTTPException):
    code = 405
    description = 'Metodo no permitido.'

