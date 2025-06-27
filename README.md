# Microservicio de Estudianes

🔹 El microservicio deEstudiantes es responsable de la gestión de usuarios tipo estudiante dentro de la plataforma. 

---


## Instalación
```bash
# Clonar el repositorio
git clone https://github.com/SumajCode/MicroService-Estudiante.git
cd tu-repo

# Instalar dependencias (ejemplo para Python)
pip install -r requirements.txt
```

## Pasos de ejecucion
```bash
# Crear un entorno virtual
python -m venv .venv
# Activar el entorno virtual (Windows)
.venv\Scripts\activate
# Activar el entorno virtual (Linux/Mac)
source .venv/bin/activate
# Ejecuccion
python main.py

```

## Configuracion de la base de datos
🔹  Cree un archivo .env y copie las variables de entorno de abajo para la conexccon a la base de datos y para el envio de correos electronicos.
```bash
# --------------------------
# MySQL conexion con (Railway) o la base de datos que utilice
# --------------------------
MYSQLUSER= 
MYSQLPASSWORD=
MYSQLHOST=
MYSQLPORT=
MYSQL_DATABASE=

# --------------------------
# Para envio de correos
# --------------------------
EMAIL_REMITENTE=micorreo@gmail.com
EMAIL_PASSWORD=    # clave de aplicaccion de google / obtener de cuenta

```

## Estructura del proyecto
```
MicroServicioEstudiante/
├── venv/                       # Entorno virtual local
├── src/                        # Código fuente del microservicio
│   ├── Bin/                    # Puntos de entrada, inicializadores
│   ├── Config/                 # Configuración general y constantes
│   ├── Domain/                 # Lógica del dominio (entidades y casos de uso)
│   ├── Features/               # Funcionalidades principales del negocio
│   ├── Infra/                  # Implementaciones técnicas (infraestructura)
│   │   ├── Controllers/        # Controladores para la lógica de negocio
│   │   ├── Email/              # Servicios de correo electrónico
│   │   ├── Events/             # Gestión de eventos del sistema
│   │   ├── Logging/            # Configuración y manejo de logs
│   │   ├── Middlewares/        # Middlewares para peticiones HTTP
│   │   ├── Models/             # Modelos de datos y ORM
│   │   ├── Routes/             # Definición de rutas y endpoints
│   │   ├── Websockets/         # Conexiones WebSocket (si aplica)
│   ├── Scripts/                # Scripts de utilidad o migraciones
│   ├── Shared/                 # Recursos compartidos (DTOs, constantes)
│   ├── Test/                   # Pruebas unitarias y de integración
├── requirements.txt            # Lista de dependencias del proyecto
└── README.md                   # Documentación del microservicio
```

## Link del deploy del la Api
```bash
# Enlace o link de la api Microservicio estudiante
https://microservice-estudiante.onrender.com

# Documento de la API, en cual explica el uso de cada ruta e incle documentacion tecnica
https://drive.google.com/drive/folders/1GAPHdObHw9YRfPB5_gli7ShqyWY883Ws?usp=sharing

```