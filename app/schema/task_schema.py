import datetime

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from ..schema.user_schema import UserResponseModel

class TaskResponseModel(BaseModel):
    id: int
    title: str
    description: str
    end_date: date
    state: str
    created_at: datetime
    user: UserResponseModel

class TaskRequestModel(BaseModel):
    title: str
    description: str
    end_date: date = datetime.now().date()

class TaskRequestPutModel(BaseModel):
    title: str
    description: str
    end_date: str = datetime.now().date()
    state: int = 0

class TaskRequestPutStateModel(BaseModel):
    state: str = 'Pending'