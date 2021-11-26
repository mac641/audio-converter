from audio_converter import models, user_datastore
import config
import datetime

models.db.create_all()

adminRole = user_datastore.create_role(name='admin',
                                       description='Administrator')
adminUser = user_datastore.create_user(email=config.MAIL_USERNAME,
                                       password=config.ADMIN_PASSWORD,
                                       active=True,
                                       confirmed_at=datetime.datetime.now())
user_datastore.add_role_to_user(user=adminUser,
                                role=adminRole)
user_datastore.create_role(name='user',
                           description='normal user')

models.db.session.commit()
