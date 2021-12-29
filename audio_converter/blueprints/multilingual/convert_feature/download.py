import glob
import os
import uuid
import zipfile

from flask_babelex import gettext
from flask_login import current_user

import audio_converter.blueprints.multilingual.utils as utils
from audio_converter import app

conversion_path = app.config['CONVERSION_PATH']
download_path = app.config['DOWNLOAD_PATH']


def zip_converted_files():
    specific_conversion_path = utils.get_audio_track_path(conversion_path)

    app.logger.info('Clean up old download files...')
    utils.delete_path(download_path)
    utils.create_path(download_path)

    app.logger.info('Start to zip all converted files...')
    download_uuid = uuid.uuid4().__str__()
    download_file = os.path.join(download_path, download_uuid + '.zip')
    try:
        with zipfile.ZipFile(download_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in glob.iglob(os.path.join(specific_conversion_path, '**/**'), recursive=True):
                if is_audio_file(file_path):
                    split_file_path = file_path.split('/')
                    file = split_file_path.pop().__str__()
                    zf.write(file_path, file)
                else:
                    app.logger.info('Skipped: ' + file_path)
    except FileNotFoundError:
        app.logger.error('Error zipping file! - ' + download_file)
        return download_file, gettext('File not found') + '!', 404

    # Delete converted files
    if not current_user.is_authenticated:
        app.logger.info('Clean up old converted files...')
        utils.delete_path(specific_conversion_path)
        utils.create_path(specific_conversion_path)

    app.logger.info('Successfully zipped all converted files!')
    return download_file, gettext('All converted files have been zipped successfully') + '!', 200


def is_audio_file(file_path):
    # TODO: Check if zipped files are audio files
    return True
