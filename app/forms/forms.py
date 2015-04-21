from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class BookForm(Form):
    '''
    Used to add a book in the website with its title, author and year of publication. Every fields are required.
    '''
    bookTitle = StringField('bookTitle', validators=[DataRequired()])
    bookAuthor = StringField('bookAuthor', validators=[DataRequired()])
    bookYear = IntegerField('bookTitle', validators=[DataRequired()])

class RegisterForm(Form):
    '''
    Used to register a new user  in the website with its pseudo, password and a confirmation of the password.
    '''
    userPseudo = StringField('userPseudo', validators=[DataRequired()])
    userPass = PasswordField('userPass', validators=[
        DataRequired(),
        EqualTo('userPassConfirm', message='Passwords must match')
    ])
    userPassConfirm = PasswordField('userPassConfirm')

class LoginForm(Form):
    '''
    Used to log a user in the website
    '''
    userPseudo = StringField('userPseudo', validators=[DataRequired()])
    userPass = PasswordField('userPass', validators=[DataRequired()])
