import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_USER = os.getenv("MYSQLUSER")
    MYSQL_PASSWORD = os.getenv("MYSQLPASSWORD")
    MYSQL_HOST = os.getenv("MYSQLHOST")
    MYSQL_PORT = os.getenv("MYSQLPORT")
    MYSQL_DB = os.getenv("MYSQL_DATABASE")
    MYSQL_ACTIVE = os.getenv("MYSQL_ACTIVE") == "True"

    
    try:
        port = int(MYSQL_PORT)
    except (TypeError, ValueError):
        port = 3306  # Puerto por defecto

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración del correo con gmail
    EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD") 


    # Configuración para ejecucion local
    HOST = os.getenv("HOST")
    PORT_API = os.getenv("PORT_API")
    ENV_DEV = os.getenv("ENV_DEV", "false").lower() == "true"
