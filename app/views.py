from flask import render_template, flash, redirect, request
from app import app, models
from .forms import BookForm

@app.route('/')
@app.route('/index')
def index():
    '''
    Lists and links every pages of the application.
    '''
    return render_template("index.html")

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    '''
    Creates a form for the user to add a new book with its title, author and year of publication.
    If the form is validated, displays entered information to the user before validation.
    '''
    form = BookForm()

    if form.validate_on_submit():
        return render_template("addBook.html", form=form, added=True)

    return render_template("addBook.html",
                           title="Add a new book",
                           form=form)

@app.route('/addBook/validate', methods=['GET', 'POST'])
def validateBook():
    '''
    Validate the entered book and add it to the database
    '''
    print request.form['title']
    if(models.addBook(request.form['title'], request.form['author'], request.form['year'])):
        flash("Book successfully added to the database.")
    else:
        flash("Book already added to the database.")
    return redirect("\index")

@app.route('/initBooks')
def initBooks():
    '''
    Initializes the database with some books
    '''
    if(models.initBooks()):
        flash("Books successfully initialized.")
    else:
        flash("Books already initialized.")
    return redirect("\index")

@app.route('/listAuthors')
def listAuthors():
    '''
    Returns a list of the registered books authors.
    '''
    list = models.getListAuthors()
    return render_template("listAuthors.html", list=list)

@app.route('/listBooks')
def listBooks():
    '''
    Returns a list of the registered books as strings.
    '''
    list = models.getListBooks()
    return render_template("listBooks.html", list=list)
