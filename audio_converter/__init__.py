from flask import Flask, request, g
# from flask_admin import Admin
from flask_migrate import Migrate
# from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from audio_converter import models

# TODO: implement database models and add to SQLAlchemy
# TODO: implement admin_models and initialize admin feature

from audio_converter import admin_models

from audio_converter import views

# TODO: initialize security feature

# Set up babel
babel = Babel(app)
@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return g.lang_code
