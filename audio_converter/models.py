# TODO: Define database models
from flask_security.models import fsqla_v2 as fsqla
from audio_converter import db


fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    def __str__(self):
        return self.name


class User(db.Model, fsqla.FsUserMixin):
    def __str__(self):
        return self.email
