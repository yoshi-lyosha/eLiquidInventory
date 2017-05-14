from website.app import db, lm
from website.app.users import constants as USER
from website.app.eliquids import constants as ELIQUID
from flask_login import UserMixin


class User(UserMixin, db.Model):

    # __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64))
    user_name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    flavors_in_inventory = db.relationship('UsersFlavoringInventory', backref='user',
                                           lazy='dynamic', cascade='all')
    nicotine_in_inventory = db.relationship('UsersNicotineInventory', backref='user',
                                            lazy='dynamic', cascade='all')
    eliquids = db.relationship('ELiquid', backref='user',
                               lazy='dynamic', cascade='all')
    favorite_eliquids = db.relationship('UsersFavouriteELiquids', backref='user',
                                        lazy='dynamic', cascade='all')

    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        return '<User %r>' % (self.user_name)


class Nicotine(db.Model):

    # __tablename__ = 'Nicotine'
    id = db.Column(db.Integer, primary_key=True)
    producer_name = db.Column(db.String(64))
    concentration = db.Column(db.SmallInteger)
    user_invs = db.relationship('UsersNicotineInventory', backref='nicotine',
                                cascade='all', lazy='dynamic')

    def __repr__(self):
        return '<Nicotine %r>' % (self.producer_name)


class Flavoring(db.Model):

    # __tablename__ = 'Flavors'
    id = db.Column(db.Integer, primary_key=True)
    flavoring_name = db.Column(db.String(64))
    producer_name = db.Column(db.String(64))
    user_invs = db.relationship('UsersFlavoringInventory', backref='flavoring',
                                cascade='all', lazy='dynamic')
    eliquids = db.relationship('ELiquidComposition', backref='flavoring',
                               cascade='all', lazy='dynamic')

    def __repr__(self):
        return '<Flavor %r Producer %r>' % (self.flavoring_name, self.producer_name)


class UsersFlavoringInventory(db.Model):

    # __tablename__ = 'Users_Flavor_Inventories'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    flavoring_id = db.Column(db.Integer, db.ForeignKey('flavoring.id'))
    amount = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<User id %r, flavor id %r, amount %r>' % (self.user_id, self.flavoring_id, self.amount)


class UsersNicotineInventory(db.Model):

    # __tablename__ = 'User_Nicotine_Inv'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    nicotine_id = db.Column(db.Integer, db.ForeignKey('nicotine.id'))
    amount = db.Column(db.SmallInteger)


class ELiquid(db.Model):

    # __tablename__ = 'eLiquids'
    id = db.Column(db.Integer, primary_key=True)
    eliquid_name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.SmallInteger, default=ELIQUID.PUBLIC)
    components = db.relationship('ELiquidComposition', backref='e_liquid',
                                 lazy='dynamic', cascade='all')
    users_fav = db.relationship('UsersFavouriteELiquids', backref='e_liquid',
                                lazy='dynamic', cascade='all')

    def __repr__(self):
        return '<Flavor %r>' % (self.eliquid_name)


class ELiquidComposition(db.Model):

    # __tablename__ = 'eLiquids_composition'
    id = db.Column(db.Integer, primary_key=True)
    eliquid_id = db.Column(db.Integer, db.ForeignKey('e_liquid.id'))
    flavoring_id = db.Column(db.Integer, db.ForeignKey('flavoring.id'))
    quantity = db.Column(db.SmallInteger)


class UsersFavouriteELiquids(db.Model):

    # __tablename__ = 'Users_Favourite_eLiquids'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    eliquid_id = db.Column(db.Integer, db.ForeignKey('e_liquid.id'))


# Users_Flavor_Inventories = db.Table('Users_Flavor_Inventories',
#                                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
#                                     db.Column('flavor_id', db.Integer, db.ForeignKey('flavor.id')),
#                                     db.Column('amount', db.SmallInteger)
#                                     )

# eLiquids_Compositions = db.Table('eLiquids_compositions',
#                                  db.Column('eliquid_id', db.Integer, db.ForeignKey('eLiquids.id')),
#                                  db.Column('flavor_id', db.Integer, db.ForeignKey('Flavors.id')),
#                                  db.Column('quantity', db.SmallInteger)
#                                  )
#

#
# Users_Nicotine_Inventories = db.Table('User_Nicotine_Inventories',
#                                       db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
#                                       db.Column('nicotine_id', db.Integer, db.ForeignKey('Nicotine.id')),
#                                       db.Column('amount', db.SmallInteger)
#                                       )
#
# Users_Favourite_ELiquids = db.Table('Users_Favourite_eLiquids',
#                                     db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
#                                     db.Column('eliquid_id', db.Integer, db.ForeignKey('eLiquids.id')),
#                                     )
