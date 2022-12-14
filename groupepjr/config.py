import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql:///{}'.format(os.path.join(BASE_DIR, 'workframe.db'))
SQLALCHEMY_MODIFICATIONS = False
SECRET_KEY = "dev"

