from peewee import *
from .settings import username_db
from .settings import password_db



database = MySQLDatabase('tasks',
                         user=username_db,
                         password=password_db,
                         host='127.0.0.1',
                         port=3306)

