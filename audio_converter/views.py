from datetime import datetime
import os.path
from flask import redirect, render_template, request, send_from_directory
from flask_security import login_required
from werkzeug.utils import secure_filename
from audio_converter import app

# TODO: decorate with multiple routes -> '/', '/index', '/logout' have to redirect to '/'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('security/login_user.html')

@app.route('/register')
def register():
    return render_template('security/register_user.html')

@app.route('/logout')
def logout():
    return render_template('home.html')

@app.route('/convert', methods=['POST', 'GET'])
def convert():
    if request.method == 'POST':
        # Do something...
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))

    return render_template('convert.html')

@app.route('/imprint')
def imprint():
    return render_template('imprint.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
