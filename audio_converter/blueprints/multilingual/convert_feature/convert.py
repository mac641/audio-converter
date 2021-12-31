import os
import subprocess
import uuid
from datetime import datetime
from pathlib import Path

from flask import g
from flask_babelex import gettext
from flask_login import current_user

import audio_converter.blueprints.multilingual.utils as utils
from audio_converter import app, db
from audio_converter.models import Track

conversion_path = app.config['CONVERSION_PATH']
upload_path = app.config['UPLOAD_PATH']
allowed_audio_file_types = app.config['ALLOWED_AUDIO_FILE_TYPES']


def process(request):
    # Ensure correct folder structure in converted
    utils.create_path(conversion_path)
    specific_conversion_path = utils.set_audio_track_path(conversion_path)
    if not current_user.is_authenticated:
        app.logger.info('Clean up old converted files...')
        utils.delete_path(specific_conversion_path)
    utils.create_path(specific_conversion_path)

    app.logger.info('Start converting all uploaded files...')
    files = utils.get_uploaded_files()

    if request.method != 'POST' or len(request.data) == 0:
        utils.delete_path(upload_path)
        utils.delete_path(specific_conversion_path)
        return gettext('The requested files can\'t be converted due to unknown destination file type') + '. ' \
               + gettext('Please select a preferred file type and try again') + '!', 400

    if len(files) == 0:
        utils.delete_path(upload_path)
        utils.delete_path(specific_conversion_path)
        return gettext('No files have been uploaded') + '. ' + gettext('Please try again') + '!', 400

    destination_file_type = str(request.data).removeprefix('b').strip('\'')
    converted_files = _filter_already_converted_files(destination_file_type)
    convertable_files = [f for f in files if f not in converted_files]

    app.logger.info('converted_files: ' + str(converted_files) + ', convertable_files: ' + str(convertable_files))

    if len(convertable_files) == 0:
        utils.move_files(upload_path, files, specific_conversion_path)

        app.logger.info('Successfully moved all uploads due to them being already converted!')
        return gettext('This conversion was successful with file type') + ': ' + destination_file_type, 301

    for file in convertable_files:
        input_file = os.path.join(upload_path, file)
        output_file = os.path.join(specific_conversion_path, Path(file).stem + destination_file_type)
        if not os.path.exists(output_file):
            subprocess.call(['ffmpeg', '-i', input_file, output_file])
            app.logger.info('Input path: ' + input_file + ', Output path: ' + output_file)

            if current_user.is_authenticated:
                g.user = current_user.get_id()
                track = Track(id=uuid.uuid4().__str__(),
                              trackname=Path(file).stem,
                              path=specific_conversion_path,
                              format=destination_file_type,
                              timestamp=datetime.now(),
                              user=g.user)
                db.session.add(track)
                db.session.commit()

    if len(converted_files) != 0:
        utils.move_files(upload_path, converted_files, specific_conversion_path)

    # Delete uploads after successful conversion
    app.logger.info('Clean up old uploads...')
    utils.delete_path(upload_path)
    utils.create_path(upload_path)

    app.logger.info('Successfully converted all uploads!')
    return gettext('This conversion was successful with file type') + ': ' + destination_file_type, 301


def _do_file_types_of_uploaded_files_match():
    suffixes = []
    # TODO: compare files using mime types
    for file in utils.get_uploaded_files():
        suffix = Path(file).suffix
        if suffix not in suffixes and suffix in allowed_audio_file_types:
            suffixes.append(suffix)

    if len(suffixes) > 1:
        return False
    return True


def _filter_already_converted_files(destination_file_type):
    filtered_files = []
    # TODO: compare files using mime types
    for file in utils.get_uploaded_files():
        suffix = Path(file).suffix
        if suffix == destination_file_type:
            filtered_files.append(file)

    return filtered_files
