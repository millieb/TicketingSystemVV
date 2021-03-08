#Importamos clase Manager de libreria flask-script
from app import create_app
from app import db, User, Ticket
from flask_script import Manager, Shell
from config import config

config_class = config['development']
app = create_app(config_class)

def make_shell_context():
    return dict(app=app, db=db, User=User, Ticket=Ticket)

if __name__ == '__main__':
    #Utilizamos la libreria flask-script para levantar el servidor
    manager = Manager(app)

    manager.add_command('shell', Shell(make_context=make_shell_context))

    manager.run()

