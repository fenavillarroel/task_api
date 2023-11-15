from sqlalchemy import Date, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..utils.db import Base
from ..utils.db import engine
from .users import User

from datetime import datetime

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    end_date = Column(Date, nullable=False)
    state = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id))

    owner = relationship("User", back_populates="items")

    def serialize(self):
        d = dict()
        d['id'] = self.id
        d['title'] = self.title
        d['description'] = self.description
        d['end_date'] = self.end_date
        d['state'] = self.state
        d['created_at'] = self.created_at
        d['user_id'] = {'id': self.user_id, 'username': self.owner.username}
        return d

Base.metadata.create_all(engine)