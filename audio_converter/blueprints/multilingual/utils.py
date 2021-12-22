import os
import shutil
from datetime import datetime

from flask import g
from flask_login import current_user

from audio_converter import app


def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


def create_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_uploaded_files(upload_path):
    files: list[str] = [f for f in os.listdir(upload_path) if os.path.isfile(os.path.join(upload_path, f))]
    return files


def move_files(source_path, files, dest_path):
    for file in files:
        # Check if file already exists in destination
        path = os.path.join(dest_path, file)
        if not os.path.exists(path):
            result = shutil.move(os.path.join(source_path, file), path)
            app.logger.info('Moved ' + result)


def get_id_day_based_path(path):
    if current_user.is_authenticated:
        g.user = current_user.get_id()
        now = datetime.now()
        create_path(os.path.join(path, g.user))
        return os.path.join(path, g.user, str(now)[:10])
    else:
        return os.path.join(path, "anonymous")

