from flask_security.models import fsqla_v2 as fsqla
from audio_converter import db

fsqla.FsModels.set_db_info(db)


class Role(db.Model, fsqla.FsRoleMixin):
    def __str__(self):
        return self.name


class User(db.Model, fsqla.FsUserMixin):
    def __str__(self):
        return self.email


class Track(db.Model):
    id = db.Column(db.String, primary_key=True)
    trackname = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    format = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    user = db.Column(db.String, nullable=False)

    def __str__(self):
        return self.trackname
