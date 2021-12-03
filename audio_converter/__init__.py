import logging

from flask import Flask, request, g, redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.menu import MenuLink
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_babelex import Babel

app = Flask(__name__)
app.config.from_object('config')

# Instantiate logging
logging.basicConfig(filename='audio-converter.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from audio_converter import models

user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app=app, datastore=user_datastore, register_blueprint=False)


# the class must be initialized before admin. Removed the normal Home button of admin model.
class DashboardView(AdminIndexView):
    def is_visible(self):
        return False

    @expose('/')
    def index(self):
        return self.render(
            '/admin/master.html'
        )


admin = Admin(app, name='Admin Audio-Converter', template_mode='bootstrap3', index_view=DashboardView())
admin.add_link(MenuLink(name='Home', url='/'))

from audio_converter import admin_models
from audio_converter.blueprints.multilingual import routes, multilingual

app.register_blueprint(multilingual)
# Set up Mail
mail = Mail(app)

# Set up Babel
babel = Babel(app)


@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return g.lang_code


@app.route('/')
def home():
    g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return redirect(url_for('multilingual.index'))

# link: https://medium.com/@nicolas_84494/flask-create-a-multilingual-web-application-with-language-specific-urls-5d994344f5fd
