#El folder app se utilizara como un modulo
#El archivo init generamos una instancia de Flask
#Definimos la funcion create_app que regresa la instancia
from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

#Creamos instancias para cada libreria
app = Flask(__name__)

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
bootstrap = Bootstrap()
login_manager = LoginManager()


#Indicamos al servidor con que rutas puede trabajar
from .views import page
from .models import User, Ticket
from .const import LOGIN_REQUIRED

#Siempre que se utilize el modulo app
#Se estara trabajando con la misma instancia
def create_app(config):
    app.config.from_object(config)

    csrf.init_app(app)

    if not app.config.get('TEST', False):
        bootstrap.init_app(app)


    
    login_manager.init_app(app)
    login_manager.login_view = '.login'
    login_manager.login_message = LOGIN_REQUIRED

    mail.init_app(app)
    
    app.register_blueprint(page)

    with app.app_context():
        #Realizamos coneccion a base de datos mediante el contexto
        db.init_app(app)
        #Creamos todas nuestras tablas
        db.create_all()
    
    return app 
