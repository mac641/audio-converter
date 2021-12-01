import os
import shutil
from pathlib import Path

from audio_converter import app

conversion_path = app.config['CONVERSION_PATH']
upload_path = app.config['UPLOAD_PATH']
allowed_audio_file_types = app.config['ALLOWED_AUDIO_FILE_TYPES']
files = [f for f in os.listdir(upload_path) if os.path.isfile(os.path.join(upload_path, f))]


def process(request):
    _delete_path(conversion_path)

    if request.method != 'POST' or len(request.data) == 0:
        return 'The requested files can\'t be converted due to unknown destination file type.' \
               'Please select a preferred file type and try again!', 400

    destination_file_type = request.data

    # converted_files = _filter_already_converted_files(destination_file_type)
    # if _do_file_types_of_uploaded_files_match() or len(converted_files) > 0:

    # Delete uploads after successful conversion
    _delete_path(upload_path)
    
    return 'file type received: ' + str(destination_file_type), 301


def _delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def _do_file_types_of_uploaded_files_match():
    suffixes = []
    for file in files:
        suffix = Path(file).suffix
        if suffix not in suffixes and suffix in allowed_audio_file_types:
            suffixes.append(suffix)

    if len(suffixes) > 1:
        return False
    return True


def _filter_already_converted_files(destination_file_type):
    filtered_files = []
    for file in files:
        suffix = Path(file).suffix
        if suffix == destination_file_type:
            filtered_files.append(file)

    return filtered_files
