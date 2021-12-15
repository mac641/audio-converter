from flask import url_for, redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from audio_converter import admin, db, models


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('/', next=request.url))


admin.add_view(AdminView(models.User, db.session))
admin.add_view(AdminView(models.Role, db.session))
