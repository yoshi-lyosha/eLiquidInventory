from app import db


flavors = db.Table('flavors',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('flavor_id', db.Integer, db.ForeignKey('flavor.id'))
                   )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    flavors = db.relationship('Flavor', secondary=flavors,
                              backref=db.backref('users', lazy='dynamic'))


class Flavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

