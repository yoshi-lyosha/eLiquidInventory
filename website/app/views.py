from flask import render_template, flash, redirect, g, url_for, session, request
from app import app, db
from app import models
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.eliquids import constants as ELIQUID


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
    if g.user is None:
        user = {'user_name': 'Guest'}
    else:
        user = g.user
    site_name = 'eLiquidInventory'
    eliquid_list = models.ELiquid.query.filter_by(status=ELIQUID.PUBLIC)
    return render_template(
        "index.html",
        title=site_name,
        user=user,
        eliquid_list=eliquid_list
    )


@app.route('/eliquids/<eliquid_id>')
def eliquid_comp(eliquid_id):
    site_name = 'eLiquidInventory'
    composition_list = models.ELiquidComposition.query.filter_by(eliquid_id=eliquid_id)
    # composition = []
    # for comp_field in composition_list:
    #         composition.append([models.Flavoring.query.filter_by(id=comp_field.flavoring_id).first(),
    #                             comp_field.quantity])
    return render_template(
        "eliquid_comp.html",
        title=site_name,
        composition=composition_list
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login form
    :return: 
    """
    if g.user is not None:
        flash('You are already logged in, {}'.format(g.user.user_name))
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('Welcome, {}'.format(user.user_name))
            print('User {} has been logged in'.format(user.user_name))
            return redirect(url_for('index'))
        else:
            flash('Email or Password are incorrect')
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
        try:
            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id
            flash('Thanks for registering, {}'.format(user.user_name))
            print('New user {} has been registered'.format(user.user_name))
            return redirect(url_for('index'))
        except Exception as e:
            if 'UNIQUE constraint failed: user.email' in str(e):
                flash('This email is already exist')
            elif 'UNIQUE constraint failed: user.user_name' in str(e):
                flash('This username is already exist')
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
        flash('For being logged out, you need to be logged in!')
        return redirect(url_for('index'))
    user = g.user
    flash('Goodbye, {}'.format(user.user_name))
    session.pop('user_id', None)
    print('User {} has been logged out. Goodbye!'.format(user.user_name))
    return redirect(url_for('index'))


@app.route('/flavorings_list')
def flavorings_list_page():
    """
    List of all flavorings
    :return: 
    """
    if g.user is None:
        user = {'user_name': 'Guest'}
    else:
        user = g.user
    site_name = 'eLiquidInventory'
    flavorings_list = models.Flavoring.query.all()

    return render_template(
        "flavorings_list.html",
        title=site_name,
        user=user,
        flavorings_list=flavorings_list
    )


@app.route('/nicotine_list')
def nicotine_list_page():
    """
    List of all nicotine
    :return: 
    """
    if g.user is None:
        user = {'user_name': 'Guest'}
    else:
        user = g.user
    site_name = 'eLiquidInventory'
    nicotine_list = models.Nicotine.query.all()

    return render_template(
        "nicotine_list.html",
        title=site_name,
        user=user,
        nicotine_list=nicotine_list
    )


@app.route('/Users/<user_name>/nickotine_inventory')
def users_nicotine_inventory(user_name):
    if g.user is None:
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    site_name = 'eLiquidInventory'
    users_nicotine_inv = models.UsersNicotineInventory.query.filter_by(user_id=g.user.id).all()
    print(users_nicotine_inv)
    return render_template(
        "user_nicotine_inventory.html",
        title=site_name,
        user=g.user,
        nicotine_inventory_list=users_nicotine_inv
    )


@app.route('/Users/<user_name>/flavorings_inventory')
def users_flavorings_inventory(user_name):
    if g.user is None:
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    site_name = 'eLiquidInventory'
    users_flavorings_inv = models.UsersFlavoringInventory.query.filter_by(user_id=g.user.id).all()
    print(users_flavorings_inv)
    return render_template(
        "user_flavorings_inventory.html",
        title=site_name,
        user=g.user,
        flavorings_inventory_list=users_flavorings_inv
    )
