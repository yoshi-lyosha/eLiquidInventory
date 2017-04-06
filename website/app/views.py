from flask import render_template, flash, redirect
from website.app import app
from website.app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'yoshi-lyosha'}
    site_name = 'eLiquidInventory'
    return render_template("index.html",
        title=site_name,
        user=user)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers = app.config['OPENID_PROVIDERS'])
