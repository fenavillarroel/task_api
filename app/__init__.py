from fastapi import FastAPI
from fastapi import APIRouter

from fastapi_pagination import add_pagination

from .utils.db import engine
from .utils.db import Base

from .model.tasks import Task
from .model.users import User

from .router.task_router import task_router
from .router.user_router import users_router

app = FastAPI(title='Tasks',
              description='Simple Tasks Manager',
              version='1.0.0')

add_pagination(app)

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(task_router)
api_v1.include_router(users_router)


app.include_router(api_v1)
