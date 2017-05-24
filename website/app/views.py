from flask import render_template, flash, redirect, g, url_for, session, request
from website.app import app, db
from website.app import models
from website.app.forms import *
from werkzeug.security import generate_password_hash, check_password_hash
from website.app.eliquids import constants as ELIQUID
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, name='eLiquidInv', template_mode='bootstrap3')
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Nicotine, db.session))
admin.add_view(ModelView(models.ELiquid, db.session))
admin.add_view(ModelView(models.ELiquidComposition, db.session))
admin.add_view(ModelView(models.Flavoring, db.session))
admin.add_view(ModelView(models.UsersFlavoringInventory, db.session))
admin.add_view(ModelView(models.UsersNicotineInventory, db.session))
admin.add_view(ModelView(models.UsersFavouriteELiquids, db.session))

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
    favourite = models.UsersFavouriteELiquids.query.filter_by(user_id=g.user.id, eliquid_id=eliquid_id).first()
    return render_template(
        "eliquid_comp.html",
        eliquid=eliquid,
        title=site_name,
        composition=composition_list,
        user=g.user,
        favourite=favourite
    )


@app.route('/like', methods=['POST'])
def like_post():
    eliquid_id = request.form.get('data')
    favourite = models.UsersFavouriteELiquids.query.filter_by(user_id=g.user.id, eliquid_id=eliquid_id).first()
    if g.user.user_name is 'Guest':
        flash('For doing this action, you need to be logged in!')
    else:
        if favourite:
            db.session.delete(favourite)
            db.session.commit()
            return ''
        else:
            new_favourite = models.UsersFavouriteELiquids(user_id=g.user.id, eliquid_id=eliquid_id)
            db.session.add(new_favourite)
            db.session.commit()
            return ''


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
                           form=form,
                           user=g.user)


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
                           form=form,
                           user=g.user)


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


@app.route('/flavorings_list', methods=['GET', 'POST'])
def flavorings_list_page():
    """
    List of all flavorings
    :return: 
    """
    form = AddFlavoringForm()
    site_name = 'eLiquidInventory'
    flavorings_list = models.Flavoring.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        if g.user.user_name is 'Guest':
                flash('For doing this action, you need to be logged in!')
        else:
            producer = request.form['producer_name']
            name = request.form['flavoring_name']
            flavoring = models.Flavoring.query.filter_by(flavoring_name=name, producer_name=producer).first()
            if flavoring:
                flash('Flavoring already exists.')
            else:
                new_flavoring = models.Flavoring(flavoring_name=name, producer_name=producer)
                db.session.add(new_flavoring)
                db.session.commit()
                return redirect('flavorings_list')

    return render_template(
        "flavorings_list.html",
        title=site_name,
        user=g.user,
        flavorings_list=flavorings_list,
        form=form,
        action="Add"
    )


@app.route("/Users/<user_name>/flavoring/<int:flavoring_id>", methods=['GET', 'POST'])
def edit_flavoring(flavoring_id, user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    flavoring = models.UsersFlavoringInventory.query.filter_by(user_id=g.user.id, flavoring_id=flavoring_id).\
        first()
    form = AddFlavoringToInvForm(obj=flavoring)
    if request.method == 'POST':
        form.populate_obj(flavoring)
        db.session.add(flavoring)
        db.session.commit()
        return redirect(url_for('users_flavorings_inventory', user_name=g.user.user_name))
    return render_template("user_flavorings_inventory.html",
                           action="Edit",

                           form=form,
                           user=g.user,
                           flavoring=flavoring.flavoring)


@app.route("/Users/<user_name>/flavoring/<int:flavoring_id>/delete", methods=['GET', 'POST'])
def delete_flavoring(flavoring_id, user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    form = AddFlavoringToInvForm()
    flavoring = models.UsersFlavoringInventory.query.filter_by(user_id=g.user.id, flavoring_id=flavoring_id).first()
    if request.method == 'POST':
        db.session.delete(flavoring)
        db.session.commit()
        return redirect(url_for('users_flavorings_inventory', user_name=g.user.user_name))
    return render_template("user_flavorings_inventory.html",
                           action="Delete",
                           user=g.user,
                           flavoring=flavoring.flavoring,
                           form=form)


@app.route("/Users/<user_name>/nicotine/<int:nicotine_id>", methods=['GET', 'POST'])
def edit_nicotine(nicotine_id, user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    nicotine = models.UsersNicotineInventory.query.filter_by(user_id=g.user.id).\
        join(models.Nicotine).\
        filter_by(id=nicotine_id).\
        first()
    form = AddNicotineToInvForm(obj=nicotine)
    if request.method == 'POST':
        form.populate_obj(nicotine)
        db.session.add(nicotine)
        db.session.commit()
        return redirect(url_for('users_nicotine_inventory', user_name=g.user.user_name))
    return render_template("user_nicotine_inventory.html",
                           action="Edit",
                           data_type=nicotine.id,
                           form=form,
                           user=g.user,
                           nicotine=nicotine.nicotine)


@app.route("/Users/<user_name>/nicotine/<int:nicotine_id>/delete", methods=['GET', 'POST'])
def delete_nicotine(nicotine_id, user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    form = AddNicotineToInvForm()
    nicotine = models.UsersNicotineInventory.query.filter_by(user_id=g.user.id, nicotine_id=nicotine_id).first()
    if request.method == 'POST':
        db.session.delete(nicotine)
        db.session.commit()
        return redirect(url_for('users_nicotine_inventory', user_name=g.user.user_name))
    return render_template("user_nicotine_inventory.html",
                           action="Delete",
                           user=g.user,
                           nicotine=nicotine.nicotine,
                           form=form)


@app.route('/nicotine_list', methods=['GET', 'POST'])
def nicotine_list_page():
    """
    List of all nicotine
    :return: 
    """
    site_name = 'eLiquidInventory'
    nicotine_list = models.Nicotine.query.all()
    form = AddNicotineForm()
    if request.method == 'POST' and form.validate_on_submit():
        if g.user.user_name is 'Guest':
                flash('For doing this action, you need to be logged in!')
        else:
            producer = request.form['producer_name']
            concentration = request.form['concentration']
            nicotine = models.Nicotine.query.filter_by(producer_name=producer, concentration=concentration).first()
            if nicotine:
                flash('Nicotine already exists.')
            else:
                new_nicotine = models.Nicotine(producer_name=producer, concentration=concentration)
                db.session.add(new_nicotine)
                db.session.commit()
                return redirect('nicotine_list')

    return render_template(
        "nicotine_list.html",
        title=site_name,
        user=g.user,
        nicotine_list=nicotine_list,
        form=form,
        action="Add"
    )


@app.route('/Users/<user_name>/nicotine_inventory', methods=['GET', 'POST'])
def users_nicotine_inventory(user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    form = AddNicotineToInvForm()
    if request.method == 'POST' and form.validate_on_submit():
        producer = request.form['producer_name']
        concentration = request.form['concentration']
        amount = request.form['amount']
        nicotine = models.Nicotine.query.filter_by(producer_name=producer,
                                                   concentration=concentration).first()
        if nicotine:
            nicotine_exists = models.UsersNicotineInventory.query.filter_by(user_id=g.user.id).\
                join(models.Nicotine).\
                filter_by(producer_name=producer,
                          concentration=concentration).\
                first()
            if nicotine_exists and nicotine_exists.amount != 0:
                flash('You have this already')
            elif nicotine_exists and nicotine_exists.amount == 0:
                flash('Updates {} by {} from {} to {}'.format(nicotine.producer_name,
                                                              nicotine.concentration,
                                                              nicotine_exists.amount,
                                                              amount))
                nicotine_exists.amount = amount
                db.session.commit()
            else:
                new_record = models.UsersNicotineInventory(nicotine_id=nicotine.id,
                                                           user_id=g.user.id,
                                                           amount=amount)
                db.session.add(new_record)
                db.session.commit()
        else:
            flash('We don\'t have this :(')

    site_name = 'eLiquidInventory'
    users_nicotine_inv = models.UsersNicotineInventory.query.filter_by(user_id=g.user.id).all()
    return render_template(
        "user_nicotine_inventory.html",
        title=site_name,
        user=g.user,
        nicotine_inventory_list=users_nicotine_inv,
        form=form,
        action="Add",
        data_type="Nicotine"
    )


@app.route('/Users/<user_name>/flavorings_inventory', methods=['POST', 'GET'])
def users_flavorings_inventory(user_name):
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    form = AddFlavoringToInvForm()
    if request.method == 'POST' and form.validate_on_submit():
        producer = request.form['producer_name']
        name = request.form['flavoring_name']
        amount = request.form['amount']
        flavoring = models.Flavoring.query.filter_by(flavoring_name=name, producer_name=producer).first()
        if flavoring:
            flavoring_exists = models.UsersFlavoringInventory.query.filter_by(user_id=g.user.id).join(models.Flavoring).filter_by(flavoring_name=name, producer_name=producer).first()
            if flavoring_exists and flavoring_exists.amount != 0:
                flash('You have this already')
            elif flavoring_exists and flavoring_exists.amount == 0:
                flash('Updates {} by {} from {} to {}'.format(flavoring.flavoring_name, flavoring.producer_name, flavoring_exists.amount, amount))
                flavoring_exists.amount = amount
                db.session.commit()
            else:
                new_record = models.UsersFlavoringInventory(flavoring_id=flavoring.id, user_id=g.user.id, amount=amount)
                db.session.add(new_record)
                db.session.commit()
        else:
            flash('We don\'t have this :(')

    site_name = 'eLiquidInventory'
    users_flavorings_inv = models.UsersFlavoringInventory.query.filter_by(user_id=g.user.id).all()
    return render_template(
        "user_flavorings_inventory.html",
        form=form,
        title=site_name,
        user=g.user,
        flavorings_inventory_list=users_flavorings_inv,
        action="Add"
    )


# @app.route('')

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


@app.route('/Users/<user_name>/eliquid_craft/<int:eliquid_id>', methods=['POST', 'GET'])
def eliquid_craft(user_name, eliquid_id):
    site_name = 'eLiquidInventory'
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('eliquid_comp', eliquid_id=eliquid_id))
    form = EliquidCraftForm()
    composition_list = models.ELiquidComposition.query.filter_by(eliquid_id=eliquid_id)
    flavorings_matching = {}
    required_flavorings_amount = {}
    new_users_flavoring_amount = {}
    ready_for_craft = True

    for composition_list_string in composition_list:
        flavoring_from_user_inv = models.UsersFlavoringInventory.query.filter_by(
            user_id=g.user.id, flavoring=composition_list_string.flavoring).first()
        flavorings_matching[composition_list_string] = flavoring_from_user_inv
        if not flavoring_from_user_inv:
            ready_for_craft = False

    craftable = True

    if ready_for_craft:
        if request.method == 'POST' and form.validate_on_submit():
            # и тут начинается матан
            quantity_of_pg = form.quantity_of_pg.data
            quantity_of_vg = form.quantity_of_vg.data
            final_amount = form.final_amount.data
            for eliquid_comp, users_flavoring in flavorings_matching.items():
                users_flavoring_amount = users_flavoring.amount
                eliquid_comp_flav_amount = eliquid_comp.quantity * final_amount * 0.01
                if users_flavoring_amount - eliquid_comp_flav_amount > 0:
                    required_flavorings_amount[eliquid_comp] = eliquid_comp_flav_amount
                    new_users_flavoring_amount[users_flavoring.id] = users_flavoring_amount - eliquid_comp_flav_amount
                else:
                    flash('You don\'t have enough; you need {} ml {} by {}, but you have only {}'.format(
                        eliquid_comp_flav_amount, eliquid_comp.flavoring.flavoring_name,
                        eliquid_comp.flavoring.producer_name, users_flavoring_amount
                    ))
                    craftable = False
            session['new_users_flavoring_amount'] = new_users_flavoring_amount
            if craftable:
                ready_for_craft = False
    else:
        flash('You can not craft this eliquid')

    if request.method == 'POST' and 'submit' in request.form:
        if request.form['submit'] == 'Done!':
            for inventory_field_id, amount in session['new_users_flavoring_amount'].items():
                user_flavoring = models.UsersFlavoringInventory.query.filter_by(id=inventory_field_id).first()
                user_flavoring.amount = amount
                db.session.add(user_flavoring)
                db.session.commit()
            session.pop('new_users_flavoring_amount', None)
            flash('Crafted!')
            ready_for_craft = False

    return render_template(
        "eliquid_craft.html",
        ready_for_craft=ready_for_craft,
        form=form,
        title=site_name,
        user=g.user,
        flavorings_matching=flavorings_matching,
        required_flavorings_amount=required_flavorings_amount,
        craftable=craftable
    )


@app.route('/Users/<user_name>/eliquid_create', methods=['POST', 'GET'])
def eliquid_create(user_name):
    site_name = 'eLiquidInventory'
    if g.user.user_name is 'Guest':
        flash('You need to be logged in for watching this page')
        return redirect(url_for('index'))
    if g.user.user_name != user_name:
        flash('Stop hecking, plz')
        return redirect(url_for('index'))
    create_eliquid_form = EliquidCreateForm()
    add_flavoring_form = AddFlavoringToEliquidForm()

    if 'new_eliquid' in session:
        new_eliquid_name = session['new_eliquid']
    else:
        new_eliquid_name = None

    if 'new_eliquid_stash_view' in session:
        new_eliquid_stash_view = session['new_eliquid_stash_view']
    else:
        new_eliquid_stash_view = None

    if request.method == 'POST' and create_eliquid_form.validate_on_submit():
        session['new_eliquid'] = create_eliquid_form.eliquid_name.data
        session['new_eliquid_status'] = create_eliquid_form.status.data
        session['new_eliquid_stash'] = {}
        session['new_eliquid_stash_view'] = []
        new_eliquid_name = session['new_eliquid']

    if request.method == 'POST' and add_flavoring_form.validate_on_submit():
        flavoring_name = add_flavoring_form.flavoring_name.data
        producer_name = add_flavoring_form.producer_name.data
        quantity = add_flavoring_form.quantity.data
        eliquid_flavoring = models.Flavoring.query.filter_by(
            flavoring_name=flavoring_name, producer_name=producer_name).first()
        if eliquid_flavoring:
            if str(eliquid_flavoring.id) not in session['new_eliquid_stash']:
                session['new_eliquid_stash'][str(eliquid_flavoring.id)] = quantity
                session['new_eliquid_stash_view'].append(
                    flavoring_name + ' by ' + producer_name + ' ' + str(quantity) + '%')
            else:
                flash('This flavoring is already in the recipe')
        else:
            flash('This flavoring does not exist')

    if request.method == 'POST' and 'submit' in request.form:
        if request.form['submit'] == 'Done!':

            e_liquid = models.ELiquid(
                eliquid_name=session['new_eliquid'], user=g.user, status=session['new_eliquid_status'])
            db.session.add(e_liquid)

            for flavoring_id, quantity in session['new_eliquid_stash'].items():
                new_flavoring = models.Flavoring.query.filter_by(id=int(flavoring_id)).first()
                component = models.ELiquidComposition(e_liquid=e_liquid, flavoring=new_flavoring, quantity=quantity)

                db.session.add(component)

            db.session.commit()

            session.pop('new_eliquid', None)
            session.pop('new_eliquid_status', None)
            session.pop('new_eliquid_stash', None)
            session.pop('new_eliquid_stash_view', None)

            flash('Created!')

    return render_template(
        "create_new_eliquid.html",
        new_eliquid_name=new_eliquid_name,
        title=site_name,
        user=g.user,
        create_eliquid_form=create_eliquid_form,
        add_flavoring_form=add_flavoring_form,
        new_eliquid_stash_view=new_eliquid_stash_view
    )
