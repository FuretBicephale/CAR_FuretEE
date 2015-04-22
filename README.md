# Conception d'application réparties - Conception d'une application web
#### Julien BRABANT - Nicolas CACHERA
###### 20/04/2015

#### Introduction

Cette application est une application web de vente de livres.

L'utilisateur peut y choisir des livres parmi une liste complète pour les ajouter dans son panier. Il lui suffira alors de valider son panier afin de valider sa commande. L'utilisateur peut aussi lister les livres par auteur ou même effectuer une recherche par titre ou année. Enfin, l'utilisateur peut voir ses commandes passées.

Un administrateur du site peut ajouter des livres à la base de donnée ou en retirer.

Cette application est une simulation de vente, aucune commande n'est réelle.

#### Architecture

Cette application comporte quatres packages.

Le package app est le package principal, contenant le script d'initialisation de l'application ainsi que les autres packages

Le package forms contient tous les formulaires utilisés dans l'application. Ces formulaires sont représentés sous forme de classe avec leurs champs de formulaires en tant qu'attribut. Toutes ces classes sont des classes filles de la classe Form proposée par Flask.

Le package models contient toutes les tables utilisées dans l'application. Ces tables sont représentées sous forme de classe avec leurs colonnes en tant qu'attribut. Toutes ces classes sont des classes filles de la classe Model proposée par SQLAlchemy.

Le package views contient toutes les requêtes disponible dans l'application. Ces requêtes sont représentées sous forme de fonction et retourne une string ou une template HTML, qui sera ensuite affichée sur la page web.
* Le module main_views contient les requêtes de la page principal, d'inscription et de connexion.
* Le module book_views contient les requêtes de création, affichage et suppression de livres.
* Le module order_views contient les requêtes d'ajout au panier d'un livre, d'affichage du panier ou des commandes, et de prise de commande.

###### Try/except
* except(ValueError) dans validateBook(), qui se declenche si l'utilisateur a renseigné autre chose qu'un entier dans le champ année lors de la saisie d'un nouveau livre. Dans ce cas, un message sera affiché à l'utilisateur pour lui indiquer son erreur.

```
try:
  if(books.addBook(request.form['title'], request.form['author'], request.form['year'])):
    flash("Book successfully added to the database.")
  else:
    flash("Book already added to the database.")
except ValueError:
  flash("Invalid year.")
  return redirect(url_for("index"))
```

#### Code Samples

Demande et renvoie de la liste des livres, filtrage par recherche inclus si demandé par l'utilisateur.

```
@app.route('/listBooks', methods=['GET', 'POST'])
def listBooks():
    title = request.args.get("title") or request.form.get("title")
    author = request.args.get("author") or request.form.get("author")
    year = request.args.get("year") or request.form.get("year")
    list = books.getListBooks(title, author, year)
    return render_template("listBooks.html", title="Books", list=list)
```

Création et renvoie de la liste des livres filtrée par recherche si besoin.

```
def getListBooks(title = None, author = None, year = None):
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
```

Validation du panier d'un utilisateur et création de la commande. La commande est liée à l'utilisateur si il est connecté.

```
@app.route('/seeCart/validateCart')
def validateCart():
    orderId = orders.addOrder(session["cart"])
    if(orderId != -1):
        if("user" in session):
            users.User.query.filter_by(pseudo=session["user"]).first().addOrder(orderId)

        flash("Order successfully validated.")
        session["cart"] = []
    else:
        flash("Something went wrong.")
    return redirect(url_for("index"))
```

Création d'une commande.

```
def addOrder(cart):
    order = Order()
    db.session.add(order)
    db.session.commit()

    for book in cart:
        if(OrderBook.query.filter_by(order_id=order.id, book_title=book).first() is None):
            orderBook = OrderBook(order.id, book)
            db.session.add(orderBook)

    db.session.commit()

    return order.id
```

Création d'un compte utilisateur.

```
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        if(users.addUser(form.userPseudo.data, form.userPass.data)):
            flash("User successfully registered.")
            return redirect(url_for("index"))
        else:
            flash("Username already used.")
            return render_template("register.html", form=form)

    return render_template("register.html",
                           title="Register",
                           form=form)
```
                           
#### Utilisation

L'application nécessite python 2 ainsi que Flask pour fonctionner.

Les modules python nécessaire à l'application s'installent grâce à la commande : pip install -r requirements.txt.

Lancement de l'application : python run.py.

L'application web sera disponible à l'adresse suivante, en local : 127.0.0.1:5000.

Lancement des tests : python tests.py.
