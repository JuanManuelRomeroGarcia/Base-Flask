from dotenv import load_dotenv
import pytz
import os


# Carga las variables de entorno desde el archivo .env
load_dotenv('.env')


class Config:
    # Configuraciones de la aplicación Flask
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    TESTING = os.getenv("TESTING", "False").lower() == "true"

    ADMIN = os.getenv("ADMIN", False)
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


    # Configuraciones de la base de datos

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuracion Carpetas
    
    # Ruta base (directorio donde se encuentra este script)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Rutas relativas
    STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static')
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Configuraciones de correo electrónico
    MAIL_DEBUG = int(os.getenv("MAIL_DEBUG", 0))
    MAIL_ADMIN = os.getenv("MAIL_ADMIN")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Idioma 
    LANGUAGES = ['en', 'es']
    BABEL_DEFAULT_LOCALE = 'es'

   # Configuración de la zona horaria
    TIMEZONE = pytz.timezone('Europe/Madrid')

    
    
