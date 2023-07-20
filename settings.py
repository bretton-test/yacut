import os
import string


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'MY_SECRET_KEY')


CHARACTERS = string.ascii_letters + string.digits
SHORT_URL_LENGTH = 6
MAIN_PAGE = 'index.html'
MAX_USER_URL_LENGTH = 16
MAX_TRY_GEN_URL = 20
