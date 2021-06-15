from flask import Flask
# from flask_admin import Admin
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from audio_converter import models

# TODO: implement database models and add to SQLAlchemy
# TODO: implement admin_models and initialize admin feature
user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

from audio_converter import admin_models

from audio_converter import views

# TODO: initialize security feature
