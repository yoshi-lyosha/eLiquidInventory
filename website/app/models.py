from website.app import db
from website.app.users import constants as USER
from website.app.eliquids import constants as ELIQUID


class User(db.Model):

    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    # нужно ли это?
    eLiquids = db.relationship('ELiquid', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Nicotine(db.Model):

    __tablename__ = 'Nicotine'
    id = db.Column(db.Integer, primary_key=True)
    producer_name = db.Column(db.String(64))
    concentration = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Nicotine %r>' % (self.producer_name)


class Flavor(db.Model):

    __tablename__ = 'Flavors'
    id = db.Column(db.Integer, primary_key=True)
    flavor_name = db.Column(db.String(64))
    producer_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Flavor %r>' % (self.flavor_name) % (self.producer_name)


class ELiquid(db.Model):

    __tablename__ = 'eLiquids'
    id = db.Column(db.Integer, primary_key=True)
    eliquid_name = db.Column(db.String(120), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.SmallInteger, default=ELIQUID.PUBLIC)

    def __repr__(self):
        return '<Flavor %r>' % (self.eliquid_name)
