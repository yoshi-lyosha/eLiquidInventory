from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import os
basedir = os.path.abspath(os.path.dirname(__file__) + '/../..')
migration_dir = os.path.abspath(os.path.join(basedir, 'host_mount/migrations'))

app = Flask(__name__)
app.config.from_object('website.config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=migration_dir)
lm = LoginManager(app)

# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'

from website.app import views, models
