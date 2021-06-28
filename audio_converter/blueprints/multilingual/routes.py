from datetime import datetime
import os.path
from flask import redirect, render_template, request, send_from_directory, Blueprint, g
from flask_babel import _, refresh
from flask_security import login_required
from werkzeug.utils import secure_filename
from audio_converter import app


multilingual = Blueprint('multilingual', __name__, template_folder='templates')


@multilingual.route('/')
@multilingual.route('/index')
def index():
    # TODO: Just for testing purposes. Remove in production.
    g.lang_code = 'de'
    refresh()
    return render_template('multilingual/index.html', title='Audio-Converter')


@multilingual.route('/convert')
def convert():
    return render_template('multilingual/convert.html', title='Audio-Converter - ' + _('Convert'))


@multilingual.route('/signin')
def signin():
    return render_template('multilingual/signin.html', title='Audio-Converter - ' + _('Sign In'))


@multilingual.route('/imprint')
def imprint():
    return render_template('multilingual/imprint.html', title='Audio-Converter - ' + _('Imprint'))


@multilingual.route('/privacy')
def privacy():
    return render_template('multilingual/privacy.html', title='Audio-Converter - ' + _('Privacy'))
