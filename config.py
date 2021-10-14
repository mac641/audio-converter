import os

from local_config import Settings

SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = Settings.SECRET_KEY
SECURITY_PASSWORD_SALT = Settings.SECURITY_PASSWORD_SALT
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CHANGEABLE = False
SECURITY_CONFIRMABLE = True
SECURITY_BLUEPRINT_NAME = 'multilingual'

SECURITY_EMAIL_SENDER = Settings.MAIL_USERNAME
SECURITY_SEND_REGISTER_EMAIL = True
SEND_PASSWORD_RESET_EMAIL = True
FLASK_ADMIN_SWATCH = 'cerulean'

MAIL_SERVER = 'smtp.web.de'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = Settings.MAIL_USERNAME
MAIL_PASSWORD = Settings.MAIL_PASSWORD

# Babel
LANGUAGES = ['en', 'de']

# Convert feature - Dropzone
UPLOAD_PATH = os.getcwd() + '/uploads'
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

DROPZONE_DEFAULT_MESSAGE = 'Drag and drop your music files here or click into the dropzone to open a file browser.'
# TODO: Change this to loading page which shows the conversion progress or index after downloading all files
DROPZONE_REDIRECT_VIEW = 'multilingual.index'
DROPZONE_TIMEOUT = 5*60*1000
DROPZONE_UPLOAD_ON_CLICK = True
DROPZONE_UPLOAD_BTN_ID='convert-upload-submit'
