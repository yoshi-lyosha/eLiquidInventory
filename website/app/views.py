from flask import render_template, flash, redirect, g, url_for, session, request
from website.app import app, db
from website.app import models
from website.app.forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from website.app.eliquids import constants as ELIQUID


@app.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = models.User.query.get(session['user_id'])
    else:
        g.user = models.User(user_name='Guest')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    site_name = 'eLiquidInventory'
    eliquid_list = models.ELiquid.query.filter_by(status=ELIQUID.PUBLIC)
    return render_template(
        "index.html",
        title=site_name,
        user=g.user,
        eliquid_list=eliquid_list
    )


@app.route('/eliquids/<eliquid_id>', methods=['POST', 'GET'])
def eliquid_comp(eliquid_id):
    site_name = 'eLiquidInventory'
    eliquid = models.ELiquid.query.filter_by(id=eliquid_id).first()
    composition_list = models.ELiquidComposition.query.filter_by(eliquid_id=eliquid_id)
    # # проверяем, есть ли эта жижка в фэйворитс
    favourite = models.UsersFavouriteELiquids.query.filter_by(user_id=g.user.id, eliquid_id=eliquid_id).first()
    # if request.method == 'POST':
    #     if g.user.user_name is 'Guest':
    #         flash('For doing this action, you need to be logged in!')
    #     else:
    #         if request.form['submit'] == 'Like it':
    #             new_favourite = models.UsersFavouriteELiquids(user_id=g.user.id, eliquid_id=eliquid_id)
    #             db.session.add(new_favourite)
    #             db.session.commit()
    #             # обновляем значение favourite для темплейта
    #             favourite = new_favourite
    #         if request.form['submit'] == 'Unlike it':
    #             db.session.delete(favourite)
    #             db.session.commit()
    #             # обновляем значение favourite для темплейта
    #             favourite = None
    return render_template(
        "eliquid_comp.html",
        eliquid=eliquid,
        title=site_name,
        composition=composition_list,
        user=g.user,
        favourite=favourite
    )


@app.route('/data', methods=['POST'])
def data_post():
    eliquid_id = request.form.get('data')
    favourite = models.UsersFavouriteELiquids.query.filter_by(user_id=g.user.id, eliquid_id=eliquid_id).first()
    if g.user.user_name is 'Guest':
        flash('For doing this action, you need to be logged in!')
    else:
        if favourite:
            db.session.delete(favourite)
            db.session.commit()
            return 'Unlike'
        else:
            new_favourite = models.UsersFavouriteELiquids(user_id=g.user.id, eliquid_id=eliquid_id)
            db.session.add(new_favourite)
            db.session.commit()
            return 'Added to favs'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login form
    :return: 
    """
    if g.user.user_name is not 'Guest':
        flash('You are already logged in, {}'.format(g.user.user_name))
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data.lower()).first()
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
    if g.user.user_name is not 'Guest':
        flash('You are already registered, {}'.format(g.user.user_name))
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = models.User(
            user_name=form.user_name.data.lower(),
            email=form.email.data.lower(),
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
    if g.user.user_name is 'Guest':
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
    # form = AddFlavoringForm()
    site_name = 'eLiquidInventory'
    flavorings_list = models.Flavoring.query.all()

    # if request.method == 'POST':
    #     if not form.validate():
    #         flash('All fields are required.')
    #         return render_template('flavorings_list.html', form=form)
    #     else:
    #         return render_template('success.html')
    # elif request.method == 'GET':
    return render_template(
        "flavorings_list.html",
        title=site_name,
        user=g.user,
        flavorings_list=flavorings_list,
        # form=form
    )


@app.route('/nicotine_list')
def nicotine_list_page():
    """
    List of all nicotine
    :return: 
    """
    site_name = 'eLiquidInventory'
    nicotine_list = models.Nicotine.query.all()

    return render_template(
        "nicotine_list.html",
        title=site_name,
        user=g.user,
        nicotine_list=nicotine_list
    )


@app.route('/Users/<user_name>/nickotine_inventory')
def users_nicotine_inventory(user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    site_name = 'eLiquidInventory'
    users_nicotine_inv = models.UsersNicotineInventory.query.filter_by(user_id=g.user.id).all()
    return render_template(
        "user_nicotine_inventory.html",
        title=site_name,
        user=g.user,
        nicotine_inventory_list=users_nicotine_inv
    )


@app.route('/Users/<user_name>/flavorings_inventory', methods=['POST', 'GET'])
def users_flavorings_inventory(user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    form = AddFlavoringToInvForm()
    if form.validate_on_submit():
        flavoring = models.Flavoring.query.filter_by(flavoring_name=form.flavoring_name.data,
                                                     producer_name=form.producer_name.data).first()
        if flavoring:
            print('Adding flavoring {} in {} inventory'.format(flavoring.flavoring_name, g.user.user_name))
            inv = models.UsersFlavoringInventory(user=g.user, flavoring=flavoring, amount=form.amount.data)
            db.session.add(inv)
            db.session.commit()
        else:
            flash("This flavoring doesn't exists in database")
    site_name = 'eLiquidInventory'
    users_flavorings_inv = models.UsersFlavoringInventory.query.filter_by(user_id=g.user.id).all()
    return render_template(
        "user_flavorings_inventory.html",
        form=form,
        title=site_name,
        user=g.user,
        flavorings_inventory_list=users_flavorings_inv
    )


@app.route('/Users/<user_name>/eliquids_inventory')
def users_favourite_eliquids(user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    site_name = 'eLiquidInventory'
    users_eliquids_inv = models.UsersFavouriteELiquids.query.filter_by(user_id=g.user.id).all()
    return render_template(
        "user_favourite_eliquids.html",
        title=site_name,
        user=g.user,
        eliquids_inventory_list=users_eliquids_inv
    )


@app.route('/Users/<user_name>/private_eliquids')
def users_private_eliquids(user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    site_name = 'eLiquidInventory'
    users_private_eliquids_list = models.ELiquid.query.filter_by(user_id=g.user.id, status=ELIQUID.PRIVATE).all()
    return render_template(
        "user_private_eliquids.html",
        title=site_name,
        user=g.user,
        private_eliquids_list=users_private_eliquids_list
    )
