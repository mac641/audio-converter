from datetime import datetime
import os.path
from flask import redirect, render_template, request, send_from_directory, Blueprint, g, abort
from flask_babelex import _
from flask_security import login_required
from werkzeug.utils import secure_filename
from audio_converter import app


multilingual = Blueprint('multilingual', __name__, template_folder='templates', url_prefix='/<lang_code>')

@multilingual.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@multilingual.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')


@multilingual.before_request
def before_request():
    if g.lang_code not in app.config['LANGUAGES']:
        abort(404)
        # TODO: create error page as HTML


@multilingual.route('/')
@multilingual.route('/index')
@multilingual.route('/logout')
def index():
    return render_template('multilingual/index.html', title='Audio-Converter', lang=g.lang_code)


@multilingual.route('/login')
def login():
    return render_template('security/login_user.html', title='Audio-Converter - ' + _('Sign In'), lang=g.lang_code)


@multilingual.route('/register')
def register():
    return render_template('security/register_user.html', title='Audio-Converter - ' + _('Register'), lang=g.lang_code)


@multilingual.route('/convert')
def convert():
    return render_template('multilingual/convert.html', title='Audio-Converter - ' + _('Convert'), lang=g.lang_code)


@multilingual.route('/imprint')
def imprint():
    return render_template('multilingual/imprint.html', title='Audio-Converter - ' + _('Imprint'), lang=g.lang_code)


@multilingual.route('/privacy')
def privacy():
    return render_template('multilingual/privacy.html', title='Audio-Converter - ' + _('Privacy'), lang=g.lang_code)
