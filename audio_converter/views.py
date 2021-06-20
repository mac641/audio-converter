from datetime import datetime
import os.path
from flask import redirect, render_template, request, send_from_directory
from flask_security import login_required
from werkzeug.utils import secure_filename
from audio_converter import app


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/convert')
def convert():
    return render_template('convert.html')


app.route('/signin')
def login():
    return render_template('signin.html')

