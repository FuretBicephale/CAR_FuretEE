from app import db
from app.models import books

def addOrder(cart):
    '''
    Add an order in the database and creates OrderBook from the content of the cart
    @type cart: list of string
    @param cart: A list of book title to add to the order
    @return The id of the order if it's done, -1 otherwise
    '''
    order = Order()
    db.session.add(order)
    db.session.commit()

    for book in cart:
        if(OrderBook.query.filter_by(order_id=order.id, book_title=book).first() is None):
            orderBook = OrderBook(order.id, book)
            db.session.add(orderBook)

    db.session.commit()

    return order.id

class OrderBook(db.Model):
    '''
    Represents the association between an order and a book with the order id and the book title
    @author cachera - brabant
    '''
    __tablename__ = "order_book"
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    book_title = db.Column(db.String, db.ForeignKey("book.title"), primary_key=True)

    def __init__(self, order_id, book_title):
        self.order_id = order_id
        self.book_title = book_title

class Order(db.Model):
    '''
    Represents a client order in the database with its id, as primary key, and books.
    @author cachera - brabant
    '''
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    books = db.relationship("OrderBook", backref="order", lazy="dynamic")

    def __repr__(self):
        '''
        Represents the order as a string
        '''
        return "Order {}".format(self.id)
