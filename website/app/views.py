from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'yoshi-lyosha'}
    site_name = 'eLiquidInventory'
    return render_template("index.html",
        title = site_name,
        user = user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html',
                           title = 'Sign In',
                           form = form)