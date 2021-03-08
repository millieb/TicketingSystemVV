import datetime

from flask_login import UserMixin

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from . import db

#Modelo para clase User, aqui podemos crear la tabla
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(94), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    tickets = db.relationship('Ticket')

    #To check password provided by the user
    def verify_password(self, password):
        return check_password_hash(self.encrypted_password, password)

    @property
    def password(self):
        pass

    @password.setter
    def password(self, value):
        self.encrypted_password = generate_password_hash(value)

    #Cada vez que se imprima un objeto de tipo user 
    #Se imprimira el username
    def __str__(self):
        return self.username

    @classmethod
    def create_element(cls, username, password, email):
        user = User(username=username, password=password, email=email)

        db.session.add(user)
        db.session.commit()

        return user

    #Method that allows to obtain a username for dupe verification
    @classmethod
    def get_by_username(cls, username):
        return User.query.filter_by(username=username).first()

    #Method that allows to obtain an email for dupe verification
    @classmethod
    def get_by_email(cls, email):
        return User.query.filter_by(email=email).first()

    #Method that allows to obtain user id
    @classmethod
    def get_by_id(cls, id):
        return User.query.filter_by(id=id).first()

#Modelo para clase Ticket, aqui podemos crear la tabla
class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text())
    company = db.Column(db.String(50))
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    @property
    def little_description(self):
        if len(self.description) > 20:
            return self.description[0:25] + "..."
        return self.description

    @classmethod
    def create_element(cls, title, description, company, category, user_id):
        ticket = Ticket(title=title, description=description, company=company, 
                        category=category, user_id=user_id)
        
        db.session.add(ticket)
        db.session.commit()

        return ticket

    @classmethod
    def get_by_id(cls, id):
        return Ticket.query.filter_by(id=id).first()

    @classmethod
    def update_element(cls, id, title, description, company, category):
        ticket = Ticket.get_by_id(id)

        if ticket is None:
            return False
        ticket.title = title
        ticket.description = description
        ticket.company = company
        ticket.category = category

        db.session.add(ticket)
        db.session.commit()

        return ticket

    @classmethod
    def delete_element(cls, id):
        ticket = Ticket.get_by_id(id)

        if ticket is None:
            return False
        db.session.delete(ticket)
        db.session.commit()

        return True
