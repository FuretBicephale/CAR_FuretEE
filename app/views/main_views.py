from flask import render_template, redirect, url_for, flash, session
from app import app
from app.forms import forms
from app.models import users

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/initUsers')
def initUsers():
    if(users.initUsers()):
        flash("Users successfully initialized.")
    else:
        flash("Users already initialized.")
    return redirect(url_for("index"))

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = users.User.query.filter_by(pseudo=form.userPseudo.data).first()
        if(user is None):
            flash("Username and password don't match.")
            session['user'] = None
            session['admin'] = None
            return render_template("login.html", form=form)
        if(user.authenticate(form.userPass.data)):
            flash("User successfully logged in.")
            session['user'] = form.userPseudo.data
            session['admin'] = user.isAdmin()
            return redirect(url_for("index"))
        else:
            flash("Username and password don't match.")
            session['user'] = None
            session['admin'] = None
            return render_template("login.html", form=form)

    return render_template("login.html",
                           title="Login",
                           form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user'] = None
    session['admin'] = None
    flash("User logged out.")
    return redirect(url_for('index'))
