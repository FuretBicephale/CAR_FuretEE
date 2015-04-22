#!flask/bin/python
import os
import unittest
from flask import url_for, session

from config import basedir
from app import app, db
from app.models import books, users, orders

class TestCase(unittest.TestCase):

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            userPseudo=username,
            userPass=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_book(self):
        # Add a book
        title = "Test"
        author = "Test"
        year = 2015

        # As admin
        self.app.get("/initUsers", follow_redirects=True)
        self.login('admin', 'admin')

        result = self.app.post("/addBook/validate", data=dict(
            title=title,
            author=author,
            year=year
            ), follow_redirects=True)

        book = books.Book.query.first()

        assert len(books.Book.query.all()) == 1
        assert book.title == title
        assert book.author == author
        assert book.year == year
        assert "Book successfully added to the database." in result.data


    def test_add_already_added_book(self):
        # Add a book which is already added
        title = "Test"
        author = "Test"
        year = 2015

        # As admin
        self.app.get("/initUsers", follow_redirects=True)
        self.login('admin', 'admin')

        books.addBook(title, author, year)
        result = self.app.post("/addBook/validate", data=dict(
            title=title,
            author="Test2",
            year=2013
            ), follow_redirects=True)

        book = books.Book.query.first()

        assert len(books.Book.query.all()) == 1
        assert book.title == title
        assert book.author == author
        assert book.year == year
        assert "Book already added to the database." in result.data

    def test_add_incorrect_year_book(self):
        # Add a book with invalid year
        title = "Test"
        author = "Test"
        year = "Test"

        # As admin
        self.app.get("/initUsers", follow_redirects=True)
        self.login('admin', 'admin')

        result = self.app.post("/addBook/validate", data=dict(
            title=title,
            author=author,
            year=year
            ), follow_redirects=True)

        assert len(books.Book.query.all()) == 0
        assert "Invalid year." in result.data

    def test_add_not_admin_book(self):
        # Add a book from a non admin user
        title = "Test"
        author = "Test"
        year = 2015

        result = self.app.post("/addBook/validate", data=dict(
            title=title,
            author=author,
            year=year
            ), follow_redirects=True)

        assert len(books.Book.query.all()) == 0

    def test_remove_book(self):
        # Remove an existing book
        title = "Test"
        author = "Test"
        year = 2015

        # As admin
        self.app.get("/initUsers", follow_redirects=True)
        self.login('admin', 'admin')

        books.addBook(title, author, year)
        result = self.app.get("/listBooks/remove?bookTitle=" + title, follow_redirects=True)

        assert len(books.Book.query.all()) == 0
        assert "Book successfully removed." in result.data

    def test_remove_unknown_book(self):
        # Remove an unexisting book
        title = "Test"
        author = "Test"
        year = 2015

        # As admin
        self.app.get("/initUsers", follow_redirects=True)
        self.login('admin', 'admin')

        books.addBook(title, author, year)
        result = self.app.get("/listBooks/remove?bookTitle=Tst", follow_redirects=True)

        book = books.Book.query.first()

        assert len(books.Book.query.all()) == 1
        assert book.title == title
        assert book.author == author
        assert book.year == year
        assert "Book not found." in result.data

    def test_remove_not_admin_book(self):
        # Remove an existing book from a non admin user
        title = "Test"
        author = "Test"
        year = 2015

        books.addBook(title, author, year)
        result = self.app.get("/listBooks/remove?bookTitle=" + title, follow_redirects=True)

        book = books.Book.query.first()

        assert len(books.Book.query.all()) == 1
        assert book.title == title
        assert book.author == author
        assert book.year == year

    def test_list_books(self):
        # List books
        self.app.get("/initBooks", follow_redirects=True)
        result = self.app.get("/listBooks")

        assert "<td>Ferret Power</td><td>Ferret Master</td><td>2016</td>" in result.data
        assert "<td>Ferret Kingdom</td><td>Ferret Master</td><td>2012</td>" in result.data
        assert "<td>The Stand</td><td>Stephen King</td><td>1990</td>" in result.data

    def test_list_empty_books(self):
        # List books when there is no books
        result = self.app.get("/listBooks")

        assert "There is no books in the database" in result.data

    def test_list_authors(self):
        # List authors
        self.app.get("/initBooks", follow_redirects=True)
        result = self.app.get("/listAuthors")

        assert "Ferret Master" in result.data
        assert "Stephen King" in result.data

    def test_list_empty_authors(self):
        # List authors when there is no books
        result = self.app.get("/listAuthors")

        assert "There is no books in the database" in result.data

    def test_list_book_per_author(self):
        # List one author's books
        self.app.get("/initBooks", follow_redirects=True)
        result = self.app.get("/listBooks?author=Ferret%20Master")

        assert "<td>Ferret Power</td><td>Ferret Master</td><td>2016</td>" in result.data
        assert "<td>Ferret Kingdom</td><td>Ferret Master</td><td>2012</td>" in result.data
        assert "<td>The Stand</td><td>Stephen King</td><td>1990</td>" not in result.data

    def test_search_books(self):
        # List books using research
        self.app.get("/initBooks", follow_redirects=True)
        result = self.app.post('/listBooks', data=dict(
            title="Ferret",
            year=2016))

        assert "<td>Ferret Power</td><td>Ferret Master</td><td>2016</td>" in result.data
        assert "<td>Ferret Kingdom</td><td>Ferret Master</td><td>2012</td>" not in result.data
        assert "<td>The Stand</td><td>Stephen King</td><td>1990</td>" not in result.data


    def test_add_user(self):
        # Add a non admin user
        username = "Test"
        password = "Test"

        result = self.app.post("/register", data=dict(
            userPseudo=username,
            userPass=password,
            userPassConfirm=password
        ), follow_redirects=True)

        user = users.User.query.first()

        assert len(users.User.query.all()) == 1
        assert user.pseudo == username
        assert user.password == password
        assert user.isAdmin() == False
        assert "User successfully registered." in result.data

    def test_add_unmatching_pass_user(self):
        # Add a non admin user with password confirmation unequals to password
        username = "Test"
        password = "Test"

        result = self.app.post("/register", data=dict(
            userPseudo=username,
            userPass=password,
            userPassConfirm="Tst"
        ), follow_redirects=True)

        assert len(users.User.query.all()) == 0
        assert "Passwords must match" in result.data


    def test_add_already_added_user(self):
        # Add a user which username is already used
        username = "Test"
        password = "Test"

        users.addUser(username, password, False)
        result = self.app.post("/register", data=dict(
            userPseudo=username,
            userPass="Test2",
            userPassConfirm="Test2"
        ), follow_redirects=True)

        user = users.User.query.first()

        assert len(users.User.query.all()) == 1
        assert user.pseudo == username
        assert user.password == password
        assert user.isAdmin() == False
        assert "Username already used." in result.data

    def test_login(self):
        # Log a user in

        # As admin
        self.app.get("/initUsers", follow_redirects=True)
        result = self.login('admin', 'admin')

        assert "Add book" in result.data
        assert "Signed in as admin" in result.data
        assert "Logout" in result.data
        assert "User successfully logged in." in result.data

        # As non admin
        username = "Test"
        password = "Test"
        users.addUser(username, password, False)
        result = self.login(username, password)

        assert "Add book" not in result.data
        assert "Signed in as Test" in result.data
        assert "Logout" in result.data
        assert "User successfully logged in." in result.data

    def test_uncorrect_username_login(self):
        # Login with an incorrect username
        self.app.get("/initUsers", follow_redirects=True)
        result = self.login('wrong', 'admin')

        assert "Add book" not in result.data
        assert "Signed in as admin" not in result.data
        assert "Register" in result.data
        assert "Login" in result.data
        assert "Username and password don&#39;t match." in result.data

    def test_unmatching_login(self):
        # Login with an incorrect password
        self.app.get("/initUsers", follow_redirects=True)
        result = self.login('admin', 'wrong')

        assert "Add book" not in result.data
        assert "Signed in as admin" not in result.data
        assert "Register" in result.data
        assert "Login" in result.data
        assert "Username and password don&#39;t match." in result.data

    def test_logout(self):
        # Log a user out
        self.app.get("/initUsers", follow_redirects=True)
        self.login('admin', 'admin')
        result = self.logout()

        assert "Add book" not in result.data
        assert "Signed in as admin" not in result.data
        assert "Register" in result.data
        assert "Login" in result.data
        assert "User logged out." in result.data

    def test_place_order(self):
        # Add books in the cart and validate the order
        self.app.get("/initBooks", follow_redirects=True)

        result = self.app.get("/listBooks/addBookToCart?bookTitle=Ferret%20Master", follow_redirects=True)
        assert "Ferret Master added to your cart." in result.data

        result = self.app.get("/listBooks/addBookToCart?bookTitle=The%20Stand", follow_redirects=True)
        assert "The Stand added to your cart." in result.data

        result = self.app.get("/seeCart/validateCart", follow_redirects=True)

        orderBooks = orders.Order.query.first().books.all()

        assert len(orders.Order.query.all()) == 1
        assert "Order successfully validated." in result.data
        for i in orderBooks:
            assert i.book_title in ["Ferret Master", "The Stand"]

    def test_see_cart(self):
        # List books added in the cart
        self.app.get("/initBooks", follow_redirects=True)

        self.app.get("/listBooks/addBookToCart?bookTitle=Ferret%20Master", follow_redirects=True)
        self.app.get("/listBooks/addBookToCart?bookTitle=The%20Stand", follow_redirects=True)
        result = self.app.get("/seeCart")

        assert "Ferret Master" in result.data
        assert "The Stand" in result.data
        assert "Ferret Kingdom" not in result.data

    def test_see_empty_cart(self):
        # See cart when it's empty
        result = self.app.get("/seeCart")

        assert "There is no books in your cart!" in result.data

    def test_list_past_order(self):
        # List past order for a user
        self.app.get("/initBooks", follow_redirects=True)

        # Order from unregistered client
        self.app.get("/listBooks/addBookToCart?bookTitle=Ferret%20Master", follow_redirects=True)
        self.app.get("/listBooks/addBookToCart?bookTitle=The%20Stand", follow_redirects=True)
        self.app.get("/seeCart/validateCart", follow_redirects=True)
        anonymousOrderId = orders.Order.query.first().id

        # Order from logged client
        self.app.get("/initUsers", follow_redirects=True)
        self.login("admin", "admin")
        self.app.get("/listBooks/addBookToCart?bookTitle=Ferret%20Master", follow_redirects=True)
        self.app.get("/listBooks/addBookToCart?bookTitle=The%20Stand", follow_redirects=True)
        self.app.get("/seeCart/validateCart", follow_redirects=True)
        loggedOrderId = orders.Order.query.filter(orders.Order.id != anonymousOrderId).first().id

        result = self.app.get("/pastOrders")

        assert "Order {}".format(loggedOrderId) in result.data
        assert "Order {}".format(anonymousOrderId) not in result.data

    def test_list_empty_past_order(self):
        # List past order for a user when it's empty
        self.app.get("/initUsers", follow_redirects=True)
        self.login("admin", "admin")
        result = self.app.get("/pastOrders")

        assert "You don't have any past order" in result.data

if __name__ == '__main__':
    unittest.main()
