import os
import shutil

from flask import g
from flask_login import current_user

from audio_converter import app
from audio_converter import db
from audio_converter.models import User

upload_path = app.config['UPLOAD_PATH']


def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)


def create_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def set_db_path(path):
    """
    Generate path based on user specific data. (Signed-In / Not Signed-In)
    Commit it to the specific user entry in the database
    Otherwise, return a folder called 'anonymous'.
    :param path: string
    :return: string
    """
    if current_user.is_authenticated:
        g.user = current_user.get_id()
        user = User.query.filter_by(fs_uniquifier=g.user).first()
        user.convert += 1
        db.session.commit()
        return os.path.join(path, g.user, str(user.convert))
    else:
        return os.path.join(path, 'anonymous')


def get_db_path(path):
    """
    Fetch a user specific path from the database.
    :param path: string
    :return: string
    """
    if current_user.is_authenticated:
        g.user = current_user.get_id()
        user = User.query.filter_by(fs_uniquifier=g.user).first()
        return os.path.join(path, g.user, str(user.convert))
    else:
        return os.path.join(path, 'anonymous')


def get_uploaded_files():
    """
    Get all files from the upload path and return them as list of strings.
    :return: <string>[]
    """
    files: list[str] = [f for f in os.listdir(upload_path) if os.path.isfile(os.path.join(upload_path, f))]
    return files


def move_files(source_path, files, dest_path):
    """
    Move files from source_path to dest_path.
    :param source_path: string
    :param files: <string>[]
    :param dest_path: string
    """
    for file in files:
        # Check if file already exists in destination
        path = os.path.join(dest_path, file)
        if not os.path.exists(path):
            result = shutil.move(os.path.join(source_path, file), path)
            app.logger.info('Moved ' + result)
