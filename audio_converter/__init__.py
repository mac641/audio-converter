from flask import Flask
from flask_admin import Admin
from flask_dropzone import Dropzone
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from audio_converter import models

# TODO: Guard admin access
# TODO: Add admin features, e.g. admin can reset user passwords, etc.
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

admin = Admin(app, name='Audio Converter', template_mode='bootstrap3')
from audio_converter import admin_models

from audio_converter import views
mail = Mail(app)

dropzone = Dropzone(app)
