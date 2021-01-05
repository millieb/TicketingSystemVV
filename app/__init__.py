#El folder app se utilizara como un modulo
#El archivo init generamos una instancia de Flask
#Definimos la funcion create_app que regresa la instancia
from flask import Flask

app = Flask(__name__)

#Indicamos al servidor con que rutas puede trabajar
from .views import page

#Siempre que se utilize el modulo app
#Se estara trabajando con la misma instancia
def create_app(config):
    app.config.from_object(config)
    app.register_blueprint(page)
    
    return app 