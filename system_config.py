import os

from flask_babelex import gettext

from media.user_config import Settings

SQLALCHEMY_DATABASE_URI = 'sqlite:///../media/database.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = Settings.SECRET_KEY
SECURITY_PASSWORD_SALT = Settings.SECURITY_PASSWORD_SALT
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = False
SECURITY_CONFIRMABLE = True
SECURITY_TRACKABLE = True
SECURITY_BLUEPRINT_NAME = 'multilingual'

SECURITY_EMAIL_SENDER = Settings.MAIL_USERNAME
SECURITY_SEND_REGISTER_EMAIL = True
SEND_PASSWORD_RESET_EMAIL = True

FLASK_ADMIN_SWATCH = 'cerulean'
ADMIN_PASSWORD = Settings.ADMIN_PASSWORD
ADMIN_ROLE_ADMIN_NAME = 'admin'
ADMIN_ROLE_ADMIN_DESCRIPTION = 'Administrator'
ADMIN_ROLE_USER_NAME = 'user'
ADMIN_ROLE_USER_DESCRIPTION = 'normal user'

MAIL_SERVER = 'smtp.web.de'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = Settings.MAIL_USERNAME
MAIL_PASSWORD = Settings.MAIL_PASSWORD

# Babel
LANGUAGES = ['en', 'de']

# Convert feature - Dropzone
UPLOAD_PATH = os.path.join(os.getcwd(), 'media', 'uploads')
CONVERSION_PATH = os.path.join(os.getcwd(), 'media', 'converted')
DOWNLOAD_PATH = os.path.join(os.getcwd(), 'media', 'downloadable')
ALLOWED_AUDIO_FILE_TYPES = [
    '.wav',
    '.flac',
    '.mp3',
    '.ogg',
    '.aiff',
    '.m4a',
]

DROPZONE_MAX_FILE_SIZE = 100
DROPZONE_ALLOWED_FILE_TYPE = 'audio'
DROPZONE_MAX_FILES = 30

DROPZONE_UPLOAD_MULTIPLE = True
DROPZONE_PARALLEL_UPLOADS = 2

DROPZONE_DEFAULT_MESSAGE = gettext('Drag and drop your music files here or click into the dropzone to open a file '
                                   'browser') + '.'
DROPZONE_TIMEOUT = 5 * 60 * 1000
