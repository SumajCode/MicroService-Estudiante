from flask import Flask, jsonify
from flask_cors import CORS 
from Config.Config import Config
from Infra.Models.EstudianteModels import db 
from Infra.Routes.EstudianteRoutes import estudiante  
from Infra.Routes.LoginRoutes import login
from Infra.Routes.RegisterLoteRoute import registrarLote
from Infra.Routes.PaisCiudadRoutes import paisCiudad
from werkzeug.exceptions import HTTPException
from flask_talisman import Talisman 

app = Flask(__name__)

# Configura CORS
Talisman(app, content_security_policy=None)  # evita redirecciones 308 en preflight
CORS(app, resources={r"/api/*": {"origins": "https://front-loginv1.vercel.app"}}, supports_credentials=True)
app.config.from_object(Config)
db.init_app(app)

# Registramos los Blueprints
app.register_blueprint(estudiante, url_prefix="/api/estudiantes")
app.register_blueprint(login, url_prefix="/api/login")
app.register_blueprint(registrarLote, url_prefix="/api/registrarLoteEstudiantes")
app.register_blueprint(paisCiudad, url_prefix="/api/")

# Ruta principal
@app.route('/')
def index():
    return "Hola esta es la API de BackendGenSof - microservicio/Estudiantes."

# Manejo de errores
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