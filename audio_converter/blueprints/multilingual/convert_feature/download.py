import os
import uuid
import zipfile

from audio_converter import app
import audio_converter.blueprints.multilingual.utils as utils

conversion_path = app.config['CONVERSION_PATH']
download_path = app.config['DOWNLOAD_PATH']


def zip_converted_files():
    utils.delete_path(download_path)
    utils.create_path(download_path)

    download_uuid = uuid.uuid4().__str__()
    download_file = os.path.join(download_path, download_uuid + '.zip')
    try:
        with zipfile.ZipFile(download_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # TODO: Adjust walking path when implementing logged in user specific features
            for dirname, sub_dirs, files in os.walk(conversion_path):
                zf.write(dirname)
                for file in files:
                    zf.write(os.path.join(dirname, file))
    except FileNotFoundError:
        app.logger.debug('Error zipping file! ' + download_file)
        return download_file, 'File not found!', 404

    app.logger.debug(download_file)
    app.logger.debug(download_uuid)
    return download_file, 'All converted files have been zipped successfully!', 200
