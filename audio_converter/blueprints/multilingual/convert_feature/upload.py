import os
from pathlib import Path

from flask_babelex import gettext

from audio_converter import app
from audio_converter.blueprints.multilingual import utils

allowed_audio_file_types = app.config['ALLOWED_AUDIO_FILE_TYPES']
upload_path = app.config['UPLOAD_PATH']


def upload(request):
    utils.create_path(upload_path)

    if request.method == 'POST':
        for key, file in request.files.items():
            if key.startswith('file'):
                if Path(file.filename).suffix not in allowed_audio_file_types:
                    return 'Only ' + ', '.join(allowed_audio_file_types) + ' allowed!', 406
                file.save(os.path.join(upload_path, file.filename))
        return gettext('Upload successful'), 200

    return gettext('There was a problem uploading your files') + '. ' + gettext('Please try again') + '!', 400
