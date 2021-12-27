import datetime

import system_config
from audio_converter import models, user_datastore

models.db.create_all()

adminRole = user_datastore.create_role(name=system_config.ADMIN_ROLE_ADMIN_NAME,
                                       description=system_config.ADMIN_ROLE_ADMIN_DESCRIPTION)
adminUser = user_datastore.create_user(email=system_config.MAIL_USERNAME,
                                       password=system_config.ADMIN_PASSWORD,
                                       active=True,
                                       confirmed_at=datetime.datetime.now())
user_datastore.add_role_to_user(user=adminUser,
                                role=adminRole)
user_datastore.create_role(name=system_config.ADMIN_ROLE_USER_NAME,
                           description=system_config.ADMIN_ROLE_USER_DESCRIPTION)

models.db.session.commit()
