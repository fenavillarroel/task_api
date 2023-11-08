from peewee import *
from .settings import username_db
from .settings import password_db
from .settings import db_host
from .settings import db_port

database = PostgresqlDatabase('tasks',
                         user=username_db,
                         password=password_db,
                         host=db_host,
                         port=db_port)

