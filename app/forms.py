from flask.ext.wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

"""
Used to add a book with its title, author and year of publication. Every fields are required.
"""
class BookForm(Form):
    bookTitle = StringField('bookTitle', validators=[DataRequired()])
    bookAuthor = StringField('bookAuthor', validators=[DataRequired()])
    bookYear = IntegerField('bookTitle', validators=[DataRequired()])
