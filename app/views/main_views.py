from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    '''
    Lists and links every pages of the application.
    '''
    return render_template("index.html")
