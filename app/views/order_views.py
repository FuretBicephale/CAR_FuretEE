from flask import render_template, redirect, session, request, url_for, flash
from app import app
from app.views import main_views, book_views
from app.models import orders, users, books

@app.route('/listBooks/addBookToCart')
def addBookToCart():
    '''
    Adds a book to the cart of the user and creates the cart if it doesn't exist.
    '''
    if(not "cart" in session):
        session["cart"] = []

    session["cart"].append(request.args.get("bookTitle"))
    flash("{} added to your cart.".format(request.args.get("bookTitle")))
    return redirect(url_for("listBooks"))

@app.route('/seeCart/removeBookFromCart')
def removeBookFromCart():
    if(not "cart" in session
            or not request.args.get("bookTitle") in session["cart"]):
        flash("Something went wrong.")
        return redirect(url_for("seeCart"))

    session["cart"].remove(request.args.get("bookTitle"))
    flash("{} removed from your cart.".format(request.args.get("bookTitle")))
    return redirect(url_for("seeCart"))

@app.route('/seeCart')
def seeCart():
    if(not "cart" in session):
        session["cart"] = []

    return render_template("seeCart.html",
                           title="Your cart",
                           cart=session["cart"])

@app.route('/seeCart/validateCart')
def validateCart():
    '''
    Validate the cart of the user and create an order, if the user is logged in, link the order to his account.
    '''
    orderId = orders.addOrder(session["cart"])
    if(orderId != -1):
        if("user" in session):
            users.User.query.filter_by(pseudo=session["user"]).first().addOrder(orderId)

        flash("Order successfully validated.")
        session["cart"] = []
    else:
        flash("Something went wrong.")
    return redirect(url_for("index"))

@app.route('/pastOrders')
def pastOrders():
    '''
    List every past orders of a logged user.
    '''
    if("user" not in session):
        return redirect(url_for("index"))

    userOrders = users.User.query.filter_by(pseudo=session["user"]).first().orders.all()

    return render_template("pastOrders.html", title="Past orders", userOrders=userOrders)

@app.route('/pastOrders/details')
def detailsOrder():
    if("user" not in session):
        return redirect(url_for("index"))

    orderBooks = orders.Order.query.filter_by(id=request.args.get("order")).first().books.all()
    detailsOrder = books.Book.query.filter(books.Book.title.in_([i.book_title for i in orderBooks])).all()

    return render_template("detailsOrder.html", title="Order details", detailsOrder=detailsOrder)
