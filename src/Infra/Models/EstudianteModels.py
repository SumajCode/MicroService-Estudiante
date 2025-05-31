from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Definimos el modelo Student, que representa la tabla "students"
class Estudiantes(db.Model):
    __tablename__ = 'estudiantes'  # Nombre de la tabla en la base de datos

    # Definimos las columnas de la tabla
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre_estudiante = db.Column(db.String(100), nullable=False)   
    apellido_estudiante = db.Column(db.String(100), nullable=False)
    correo_estudiante = db.Column(db.String(100), nullable=False)
    contrasenia = db.Column(db.String(200), nullable=False) #no se mostrara
    fecha_registro = db.Column(db.DateTime, nullable=False)    
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    numero_celular = db.Column(db.String(100), nullable=False)
    fecha_ultimo_acceso = db.Column(db.DateTime)
    es_universitario = db.Column(db.Boolean, nullable=False, default=False)
    id_pais = db.Column(db.Integer, nullable=False)
    id_ciudad = db.Column(db.Integer, nullable=False)


    # Método para convertir el objeto a diccionario, útil para retornar JSON
    def to_dict(self):
        return {"id_estudiante": self.id_estudiante,
                "nombre_estudiante": self.nombre_estudiante,
                "apellido_estudiante": self.apellido_estudiante,
                "correo_estudiante": self.correo_estudiante,
                "contrasenia": self.contrasenia, 
                "fecha_registro": self.fecha_registro,
                "fecha_nacimiento": self.fecha_nacimiento, 
                "numero_celular": self.numero_celular,
                "fecha_ultimo_acceso": self.fecha_ultimo_acceso, 
                "es_universitario": self.es_universitario,
                "id_pais": self.id_pais, 
                "id_ciudad": self.id_ciudad}  
        
        