from flask import Flask, jsonify
from Config.Config import Config
from Infra.Models.EstudianteModels import db 
from Infra.Routes.EstudianteRoutes import estudiante  
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
# Registramos el Blueprint que contiene las rutas de estudiantes
app.register_blueprint(estudiante, url_prefix="/api/estudiantes")


# Ruta principal o por defecto
@app.route('/')
def index():
    return "Hola esta es la API de BackendGenSof - microservicio/Estudiantes."

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "status": 404,
        "message": "La ruta solicitada no existe. Verifica la URL y el método."
    }), 404


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({
        "status": e.code,
        "message": e.description
    }), e.code


if __name__ == '__main__':
    app.run(debug=True)
