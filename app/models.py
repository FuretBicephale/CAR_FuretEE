from app import db

def initBooks():
    '''
    Initializes the database with some books and return True if it's done, False if it was already done.
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
    list = []
    books = Book.query.all()
    for book in books:
        if(list.count(book.author) == 0):
            list.append(book.author)
    return list

class Book(db.Model):
    '''
    Represents a Book in the database with its title, as primary key, author and publication year.
    '''
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
        return "[{}] {} by {}".format(year, title, author)
