from flask import render_template, redirect, session, request, url_for, flash
from app import app
from app.views import main_views, book_views
from app.models import orders

@app.route('/listBooks/addBookToCart')
def addBookToCart():
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
    if(orders.addOrder(session["cart"])):
        flash("Order successfully validated.")
        session["cart"] = []
    else:
        flash("Something went wrong.")
    return redirect("index")
