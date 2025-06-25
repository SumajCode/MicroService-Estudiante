from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_talisman import Talisman
from Config.Config import Config
from Infra.Models.EstudianteModels import db
from Infra.Routes.EstudianteRoutes import estudiante
from Infra.Routes.LoginRoutes import login
from Infra.Routes.RegisterLoteRoute import registrarLote
from Infra.Routes.PaisCiudadRoutes import paisCiudad
from werkzeug.exceptions import HTTPException

def crearApp():
    app = Flask(__name__)

    # Seguridad HTTPS: No forzar redirección aquí para evitar conflicto con CORS
    Talisman(app, content_security_policy=None, force_https=False)

    # CORS para todas las rutas, permitiendo todos los orígenes sin credenciales
    CORS(app)

    app.config.from_object(Config)
    db.init_app(app)

    api_blueprint = Blueprint('api', __name__, url_prefix='/api')

    @api_blueprint.route('/')
    def home():
        return jsonify({
            'data': f"{app.config.get('APP_NAME', 'BackendGenSof')} - Microservicio Estudiantes",
            'message': 'API en funcionamiento',
            'status': 200
        })

    # Registro de rutas hijas con prefijos explícitos
    api_blueprint.register_blueprint(estudiante, url_prefix="/estudiantes")
    api_blueprint.register_blueprint(login, url_prefix="/login")
    api_blueprint.register_blueprint(registrarLote, url_prefix="/registrarLoteEstudiantes")
    api_blueprint.register_blueprint(paisCiudad, url_prefix="")

    app.register_blueprint(api_blueprint)

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "status": 404,
            "message": "La ruta solicitada no existe. Verifica la URL y el método.",
            "error": str(error)
        }), 404

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return jsonify({
            "status": e.code,
            "message": e.description,
            "error": str(e)
        }), e.code

    return app
