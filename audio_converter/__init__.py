from flask import Flask
# from flask_admin import Admin
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: implement database models and add to SQLAlchemy
# TODO: initialize security feature

# TODO: implement admin_models and initialize admin feature


