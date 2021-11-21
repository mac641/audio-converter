import os
import shutil

from audio_converter import app

def process(request):
    conversion_path = app.config['CONVERSION_PATH']
    if os.path.isdir(conversion_path):
        shutil.rmtree(conversion_path)
    os.mkdir(conversion_path)

    if request.method != 'POST' or len(request.data) == 0:
        return 'The requested files can\'t be converted due to unknown destination file type.' \
               'Please select a preferred file type and try again!', 400

    file_type = request.data

    return 'file type received: ' + str(file_type), 200
