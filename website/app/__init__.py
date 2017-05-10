from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('website.config')
db = SQLAlchemy(app)
<<<<<<< HEAD
migrate = Migrate(app, db, directory='website/host_mount/migrations')
=======
migrate = Migrate(app, db)
lm = LoginManager(app)
>>>>>>> d7b14fda0004aa5d8877280e12dd8908b5533873

# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'

from website.app import views, models
