import os
import subprocess
from pathlib import Path

from audio_converter import app
import audio_converter.blueprints.multilingual.utils as utils

conversion_path = app.config['CONVERSION_PATH']
upload_path = app.config['UPLOAD_PATH']
allowed_audio_file_types = app.config['ALLOWED_AUDIO_FILE_TYPES']


def process(request):
    utils.delete_path(conversion_path)
    utils.create_path(conversion_path)

    files = utils.get_uploaded_files(upload_path)

    if request.method != 'POST' or len(request.data) == 0:
        return 'The requested files can\'t be converted due to unknown destination file type.' \
               'Please select a preferred file type and try again!', 400

    if len(files) == 0:
        return 'No files have been uploaded. Please try again!', 400

    destination_file_type = str(request.data).removeprefix('b').strip('\'')
    converted_files = _filter_already_converted_files(destination_file_type)
    convertable_files = [f for f in files if f not in converted_files]

    app.logger.debug('converted_files: ' + str(converted_files) + ', convertable_files: ' + str(convertable_files))

    for file in convertable_files:
        input_file = os.path.join(upload_path, file)
        output_file = os.path.join(conversion_path, Path(file).stem + destination_file_type)
        return_code = subprocess.call(['ffmpeg', '-i', input_file, output_file])
        app.logger.debug('Input path: ' + input_file + ', Output path: ' + output_file)

    # Delete uploads after successful conversion
    utils.delete_path(upload_path)
    utils.create_path(upload_path)

    return 'conversion was successful with file type: ' + destination_file_type, 301


def _do_file_types_of_uploaded_files_match():
    suffixes = []
    for file in utils.get_uploaded_files(upload_path):
        suffix = Path(file).suffix
        if suffix not in suffixes and suffix in allowed_audio_file_types:
            suffixes.append(suffix)

    if len(suffixes) > 1:
        return False
    return True


def _filter_already_converted_files(destination_file_type):
    filtered_files = []
    for file in utils.get_uploaded_files(upload_path):
        suffix = Path(file).suffix
        if suffix == destination_file_type:
            filtered_files.append(file)

    return filtered_files
