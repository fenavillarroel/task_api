from peewee import *
from datetime import  datetime

from ..utils.db import database

from .users import User

class Task(Model):
    title = CharField(max_length=128, null=False)
    description = CharField(max_length=255, null=False)
    end_date = DateField(null=False)
    state = IntegerField(default=0, null=False)
    created_at = DateField(default=datetime.now())
    user = ForeignKeyField(User, backref='tasks')

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = 'tasks'