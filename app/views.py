#en este archivo definimos rutas y funciones asociadas
from flask import Blueprint         #importamos clases
from flask import render_template   #importamos funciones

page = Blueprint('page', __name__)

#definimos nueva ruta que respondera cuando haya un error 404
@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

#definimos nueva ruta index para responder peticiones
@page.route('/')
def index():
    return render_template('index.html')