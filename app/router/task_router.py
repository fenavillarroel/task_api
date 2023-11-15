from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session

from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

from ..schema.task_schema import TaskResponseModel
from ..schema.task_schema import TaskRequestModel
from ..schema.task_schema import TaskRequestPutModel
from ..schema.task_schema import TaskRequestPutStateModel
from ..schema.task_schema import TaskDeleteResponseModel

from ..utils.settings import TASK_STATES
from ..utils.db import get_db

from ..model.users import User
from ..model.tasks import Task

from ..utils.tokens import get_current_user

task_router = APIRouter(prefix='/tasks')

state_decription = description = """
### Valid States
- 0: Pending
- 1: Progress
- 2: Complete
- 3: Cancel
"""

@task_router.post('', response_model=TaskResponseModel)
async def create_task(user_task: TaskRequestModel,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):

    user_task = Task(
        title = user_task.title,
        description = user_task.description,
        end_date = user_task.end_date,
        user_id = user.id
    )

    db.add(user_task)
    db.commit()
    db.refresh(user_task)

    user_task.state = TASK_STATES[user_task.state]

    return user_task


@task_router.get('', response_model=Page[TaskResponseModel])
async def get_tasks(user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):

    user_tasks = db.query(Task).filter(Task.user_id == user.id)
    for task_user in user_tasks:
        task_user.state = TASK_STATES[task_user.state]

    return paginate(user_tasks)


@task_router.get('/{task_id}', response_model=TaskResponseModel)
async def get_task(task_id: int,
                    user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):

    user_task = db.query(Task).filter(Task.id == task_id).one_or_none()

    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    if user_task.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Task is different')

    user_task.state = TASK_STATES[user_task.state]

    return user_task

@task_router.put('/{task_id}', response_model=TaskResponseModel)
async def update_task(task_id: int,
                        task_request: TaskRequestPutModel,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db),
                        description = state_decription):

    user_task = db.query(Task).filter(Task.id == task_id).first()

    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    if user_task.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Task is different')

    try:
        state = TASK_STATES[task_request.state]
    except:
        raise HTTPException(status_code=404, detail='Code State Not found')

    user_task.state = task_request.state
    user_task.title = task_request.title
    user_task.description = task_request.description
    user_task.end_date = task_request.end_date

    db.commit()
    db.refresh(user_task)

    user_task.state = TASK_STATES[task_request.state]

    return user_task


@task_router.put('/states/{task_id}', response_model=TaskResponseModel)
async def update_task_state(task_id: int,
                        task_request: TaskRequestPutStateModel,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db),
                        description = state_decription):
    try:
        state = list(TASK_STATES.values()).index(task_request.state)
    except:
        raise HTTPException(status_code=404, detail='State Name Not found')

    user_task = db.query(Task).filter(Task.id == task_id).one_or_none()
    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    user_task.state = state
    db.commit()
    db.refresh(user_task)

    user_task.state = TASK_STATES[state]

    return user_task


@task_router.delete('/{task_id}', response_model=TaskDeleteResponseModel)
async def delete_task(task_id: int,
                        db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):

    user_task = db.query(Task).filter(Task.id == task_id).one_or_none()

    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    if user_task.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Task is different')

    db.delete(user_task)
    db.commit()
    user_task.state = TASK_STATES[user_task.state]

    return user_task
