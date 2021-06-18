from flask_admin.contrib.sqla import ModelView
from audio_converter import admin, db, models

admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Role, db.session))
