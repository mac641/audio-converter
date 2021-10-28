import os
import shutil
from pathlib import Path

from audio_converter import app

allowed_audio_file_types = app.config['ALLOWED_AUDIO_FILE_TYPES']

def upload(request):
    upload_path = app.config['UPLOAD_PATH']
    if os.path.isdir(upload_path):
        shutil.rmtree(upload_path)
    os.mkdir(upload_path)

    if request.method == 'POST':
        for key, file in request.files.items():
            if key.startswith('file'):
                if Path(file.filename).suffix not in allowed_audio_file_types:
                    return 'Only' + ', '.join(allowed_audio_file_types) + 'allowed!', 406
                file.save(os.path.join(upload_path, file.filename))
        return 'Upload successful', 200

    return 'There was a problem uploading your files. Please try again!', 400
