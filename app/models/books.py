from app import db

def initBooks():
    '''
    Initializes the database with some books and return True if it's done, False if it was already done.
    @return True if books are successfully initialized, false otherwise.
    '''
    if(not(Book.query.filter_by(title='Ferret Power').first() is None)):
        return False

    b1 = Book("Ferret Power", "Ferret Master", 2016);
    b2 = Book("Ferret Kingdom", "Ferret Master", 2012);
    b3 = Book("The Stand", "Stephen King", 1990);

    db.session.add(b1)
    db.session.add(b2)
    db.session.add(b3)

    db.session.commit()

    return True

def getListAuthors():
    '''
    Return a list of string containing every author of books in database, without duplication
    @return A list of string containing authors
    '''
    list = []
    books = Book.query.all()
    for book in books:
        if(list.count(book.author) == 0):
            list.append(book.author)
    return list

def getListBooks(title = None, author = None, year = None):
    '''
    Return a list of Book containing every book in database
    @type title: string
    @param title: If it's not None, filter the book on its title
    @type author: string
    @param author: If it's not None, filter the book on its author
    @type year: number
    @param year: If it's not None, filter the book on its year
    @return A list of Book object
    '''
    list = []
    books = Book.query
    if(title != None and title != ""):
        books = books.filter(Book.title.contains(title))
    if(author != None and author != ""):
        books = books.filter(Book.author.contains(author))
    if(year != None and year != ""):
        books = books.filter_by(year = year)
    for book in books.all():
        list.append(book)
    return list

def addBook(title, author, year):
    '''
    Add a book to the database with its title, author and year and return True if it's done.
    @type title: string
    @type author: string
    @type year: number
    @return True if the book is added, False otherwise
    '''
    if(Book.query.filter_by(title=title).first() is not None):
        return False

    b = Book(title, author, year)
    db.session.add(b)
    db.session.commit()

    return True

def removeBook(title):
    '''
    Remove the book with title as title and return True if it's done
    @type title: string
    @return True if the book is found and removed, False otherwise
    '''
    book = Book.query.filter_by(title=title).first()
    if(book is None):
        return False

    db.session.delete(book)
    db.session.commit()

    return True

class Book(db.Model):
    '''
    Represents a Book in the database with its title, as primary key, author and publication year.
    @author cachera - brabant
    '''
    _tablename__ = "book"
    title = db.Column(db.String(64), primary_key=True)
    author = db.Column(db.String(64))
    year = db.Column(db.Integer)

    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        '''
        Represents the book as a string
        '''
        return "[{}] {} by {}".format(self.year, self.title, self.author)
