from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: implement database models and add to SQLAlchemy
# TODO: initialize security feature

# TODO: implement admin_models and initialize admin feature


