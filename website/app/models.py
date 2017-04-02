from website.app import db
from website.app.users import constants as USER

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):

    __tablename__ = 'totally_not_users_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)

    def __repr__(self):
        return '<User %r>' % (self.nickname)
