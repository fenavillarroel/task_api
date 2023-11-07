from fastapi import FastAPI
from fastapi import APIRouter
from app.utils.db import database as cnx

from .model.tasks import Task
from .model.users import User

from .router.task_router import task_router
from .router.user_router import users_router

app = FastAPI(title='Tasks',
              description='Simple Tasks Manager',
              version='1.0.0')

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(task_router)
api_v1.include_router(users_router)


app.include_router(api_v1)

@app.on_event('startup')
def startup():
    if cnx.is_closed():
        cnx.connect()

    cnx.create_tables([User, Task])

@app.on_event('shutdown')
def shotdown():
    if not cnx.is_closed():
        cnx.close()
        print('Disconnected....')