from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'

from app import views, models
