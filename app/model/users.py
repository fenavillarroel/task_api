from peewee import *
from datetime import datetime
import hashlib
from ..utils.db import database


class User(Model):
    username = CharField(max_length=50, unique=True, null=False)
    password = CharField(max_length=50, null=False)
    created_at = DateField(default=datetime.now())

    def __str__(self):
        return self.username

    @staticmethod
    def create_password(password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        user = cls.select().where(User.username == username).first()
        if user and user.password == cls.create_password(password):
            return user

        return None

    def serialize(self):
        d = dict()
        d['id'] = self.id
        d['username'] = self.username
        return d

    class Meta:
        database = database
        table_name = 'users'

