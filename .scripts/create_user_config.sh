#!/bin/bash

set -e

if [ -f ./media/user_config.py ];
then
  echo "RESULT: File exists"
else
cat << EOF > media/user_config.py
class Settings:
    MAIL_PASSWORD = '********'  # Enter the password of your mail server.
    MAIL_USERNAME = 'example@example.com'  # Enter the email address of your mail server.
    SECRET_KEY = 'secretkey'  # Enter a safety secretkey.
    SECURITY_PASSWORD_SALT = 'secretsalt'  # Enter a safety secretsalt.
    ADMIN_PASSWORD = '********'  # Enter an individual password for the admin account."
EOF
echo "RESULT: File created" 
fi
