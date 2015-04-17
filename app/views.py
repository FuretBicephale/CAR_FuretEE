from flask import render_template
from app import app
from .forms import BookForm

@app.route('/')
@app.route('/index')
def index():
    """
    Lists and links every pages of the application.
    """
    return render_template("index.html")

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    """
    Creates a form for the user to add a new book with its title, author and year of publication.
    If the form is validated, displays entered information to the user before validation.
    """
    form = BookForm()

    if form.validate_on_submit():
        return render_template('addBook.html', form=form, added=True)

    return render_template('addBook.html',
                           title='Add a new book',
                           form=form)
