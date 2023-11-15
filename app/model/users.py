from fastapi import Depends

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from ..utils.db import Base
from ..utils.db import engine
from ..utils.db import session

from datetime import datetime
import hashlib

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    items = relationship("Task", back_populates="owner")

    @staticmethod
    def create_password(password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        user = session.query(cls).filter(cls.username == username).first()
        if user and user.password == cls.create_password(password):
            return user

        return None

    def serialize(self):
        d = dict()
        d['id'] = self.id
        d['username'] = self.username
        return d

Base.metadata.create_all(engine)