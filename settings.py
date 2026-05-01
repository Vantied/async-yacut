import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DB')
    SECRET_KEY = os.getenv('SECRET_KEY')
    DISK_TOKEN = os.getenv('DISK_TOKEN')
