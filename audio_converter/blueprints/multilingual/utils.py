import os
import shutil
from datetime import datetime

from flask import g
from flask_login import current_user


def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    create_path(path)


def create_path(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_uploaded_files(upload_path):
    files: list[str] = [f for f in os.listdir(upload_path) if os.path.isfile(os.path.join(upload_path, f))]
    return files


def get_id_day_based_path(path):
    if current_user.is_authenticated:
        g.user = current_user.get_id()
        now = datetime.now()
        create_path(path + "/" + g.user)
        return path + "/" + g.user + "/" + str(now)[:10]
    else:
        return path + "/anonymous"

