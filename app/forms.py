from wtforms import Form, HiddenField
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from .models import User

#Esta funcion nos permite validar un campo
#This is a test validator
def codi_validator(form, field):
    if field.data == 'codi' or field.data == 'Codi':
        raise validators.ValidationError('Username codi is not allowed.')

#Function validating honeypot. If it has values it raises an error
def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Only humans can complete register form.')

#Esta clase nos permitira generar nuesto formulario de login
class LoginForm(Form):
    username = StringField('Username', [
        validators.length(min=4, max=50)
    ])
    password = PasswordField('Password', [
        validators.Required(message='Password is required')
    ])

#Esta clase nos permitira generar nuestro formulario de Register
class RegisterForm(Form):
    username = StringField('Username', [
        validators.length(min=4, max=50),
        codi_validator
    ])
    email = EmailField('Email', [
        validators.length(min=6, max=100),
        validators.Required(message='Email is required.'),
        validators.Email(message='Enter a valid email.')
    ])
    password = PasswordField('Password', [
        validators.Required('Password is required.'),
        validators.EqualTo('confirm_password', message='Passwords are not equal.')
    ])
    confirm_password = PasswordField('Confirm Password')
    accept = BooleanField('', [
        validators.DataRequired()
    ])

    #New hidden field to prevent creation of thousands of valid accounts at once
    honeypot = HiddenField("", [length_honeypot])

    #To validate username
    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError('Username is already in use.')

    #To validate email
    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError('Email is already in use.')

    #Overwriting validate function
    def validate(self):
        #Returns false if a field does not meet at least 1 validation
        if not Form.validate(self):
            return False
        
        #Validates password is > 2 chars
        if len(self.password.data) < 3:
            self.password.errors.append('Password does not meet length requirements')
            return False

        return True

#Formulario de Tickets
class TicketForm(Form):
    title = StringField('Title', [
        validators.length(min=4, max=50, message='Title outside of range.'),
        validators.DataRequired(message='Title is required.')
    ])
    description = TextAreaField('Description', [
        validators.DataRequired(message='Description is required.')
    ], render_kw={'rows': 5})
    company = SelectField(
        'Company',
        choices=[('DX', 'DataXport'), ('OV', 'Oveana')])
    category = SelectField(
        'Category',
        choices=[('PR', 'Password Reset'), ('HW', 'Hardware'), ('SW', 'Software'),
                 ('AWS', 'Awazon WorkSpaces'), ('MN', 'Maintenance')])
