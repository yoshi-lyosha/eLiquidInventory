from flask import render_template, flash, redirect, g, url_for, session, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from website.app import app, db, models
from website.app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = models.User.query.get(session['user_id'])


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # if "flask_login.mixins.AnonymousUserMixin object" in str(g.user):
    # print(session['user_id'])
    if g.user is None:
        user = {'user_name': 'Guest'}
    else:
        user = g.user
    site_name = 'eLiquidInventory'
    return render_template(
        "index.html",
        title=site_name,
        user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login form
    :return: 
    """
    if g.user is not None:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome, {}'.format(user.user_name))
            return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Sign up form
    :return: 
    """
    if g.user is not None:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = models.User(
            user_name=form.user_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        flash('Thanks for registering, {}'.format(user.user_name))
        return redirect(url_for('index'))
    return render_template("register.html",
                           title='Sign up',
                           form=form)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Loging out form
    :return: 
    """
    if g.user is None:
        return redirect(url_for('index'))
    user = g.user
    flash('Goodbye, {}'.format(user.user_name))
    session.pop('user_id', None)
    return redirect(url_for('index'))
