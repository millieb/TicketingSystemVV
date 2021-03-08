#en este archivo definimos rutas y funciones asociadas
from flask import Blueprint                            #importamos clases
from flask import render_template, request, flash, redirect, url_for, abort   #importamos funciones

from flask_login import login_user, logout_user, login_required, current_user 

from .models import User, Ticket
from .forms import LoginForm, RegisterForm, TicketForm
from . import login_manager
from .const import *
from .email import welcome_mail

page = Blueprint('page', __name__)

#Receives user id as a parameter
@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)

#definimos nueva ruta que respondera cuando haya un error 404
@page.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

#definimos nueva ruta index para responder peticiones
@page.route('/')
def index():
    return render_template('index.html', title='Index')

#define new url route to close session
@page.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT)
    return redirect(url_for('.login'))

#definimos nueva ruta para formulario login
@page.route('/login', methods=['GET', 'POST'])
def login():

    #authenticated users are redirected to tickets website
    if current_user.is_authenticated:
        return redirect(url_for('.tickets')) 

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        # obtain username based on user
        user = User.get_by_username(form.username.data)
        if user and user.verify_password(form.password.data):     # verifies user input password and user
            login_user(user)
            flash(LOGIN)
            return redirect(url_for('.tickets'))
        else:
            flash(ERROR_USER_PASSWORD, 'error')

    return render_template('auth/login.html', title='Login', form=form,
                            active='login')

#definimos nueva ruta para formulario register
@page.route('/register', methods=['GET', 'POST'])
def register():

    #authenticated users are redirected to tickets website
    if current_user.is_authenticated:
        return redirect(url_for('.tickets'))

    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate():
            user = User.create_element(form.username.data, form.password.data, form.email.data)
            flash(USER_CREATED)
            login_user(user)
            welcome_mail(user)
            return redirect(url_for('.tickets'))

    return render_template('auth/register.html', title='Register',
                            form=form, active='register')

#New route for tickets
@page.route('/tickets')
@login_required
def tickets():
    tickets = current_user.tickets
    return render_template('tickets/list.html', title='Tickets', tickets=tickets,
                            active='tickets')

@page.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    form = TicketForm(request.form)

    if request.method == 'POST' and form.validate(): 
        ticket = Ticket.create_element(
            form.title.data, 
            form.description.data, 
            form.company.data, 
            form.category.data, 
            current_user.id)
        
        if ticket:
            flash(TICKET_CREATED)

    return render_template('tickets/new.html', title='New Ticket', 
                            form=form, active='new_ticket')

#To show ticket details
@page.route('/tickets/show/<int:ticket_id>')
def get_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    return render_template('tickets/show.html', title='Ticket', ticket=ticket)

#To edit ticket
@page.route('/tickets/edit/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.user_id != current_user.id:
        abort(404)

    form = TicketForm(request.form, obj=ticket) #obj populates information in ticket
    if request.method == 'POST' and form.validate():
        ticket = ticket.update_element(ticket.id, 
                                        form.title.data,
                                        form.description.data,
                                        form.company.data,
                                        form.category.data)
        if ticket:
            flash(TICKET_UPDATED)

    return render_template('tickets/edit.html', title='Edit Ticket', form=form)

#To delete ticket
@page.route('/tickets/delete/<int:ticket_id>')
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.user_id != current_user.id:
        abort(404)

    if Ticket.delete_element(ticket.id):
        flash(TICKET_DELETED)

    return redirect(url_for('.tickets'))
