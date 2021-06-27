from datetime import datetime
import os.path
from flask import redirect, render_template, request, send_from_directory
from flask_security import login_required
from werkzeug.utils import secure_filename
from audio_converter import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Audio-Converter')


@app.route('/convert')
def convert():
    return render_template('convert.html', title='Audio-Converter - Convert')


@app.route('/signin')
def signin():
    return render_template('signin.html', title='Audio-Converter - Sign In')


@app.route('/imprint')
def imprint():
    return render_template('imprint.html', title='Audio-Converter - Imprint')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Audio-Converter - Privacy')
