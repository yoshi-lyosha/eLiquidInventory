from app import app
from flask import render_template, flash, redirect
from user import User
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    fedos = User('Fedos')
    fedos.add_flavor('strawberry', 15)
    fedos.add_flavor('pineapple', 20)
    return render_template('index.html',
                           user=fedos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="{}", remember_me={}'.format(form.openid.data, str(form.remember_me.data)))
        return redirect('/login.html')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])