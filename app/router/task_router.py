from typing import List
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from ..schema.task_schema import TaskResponseModel
from ..schema.task_schema import TaskRequestModel
from ..schema.task_schema import TaskRequestPutModel
from ..schema.task_schema import TaskRequestPutStateModel

from ..utils.settings import task_states
from ..utils.settings import page
from ..utils.settings import limit_page

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
                        user: User = Depends(get_current_user)):

    user_task = Task.create(
        title = user_task.title,
        description = user_task.description,
        end_date = user_task.end_date,
        user_id = user.id
    )

    return TaskResponseModel(
        id=user_task.id,
        title=user_task.title,
        description=user_task.description,
        end_date=user_task.end_date,
        state=task_states[user_task.state],
        created_at=user_task.created_at,
        user=user.serialize()
    )

@task_router.get('', response_model=List[TaskResponseModel])
async def get_tasks(user: User = Depends(get_current_user),
                      page: int = page,
                      limit: int = limit_page):

    user_tasks = Task.select().where(Task.user_id == user.id).paginate(page, limit)
    for user_task in user_tasks:
        user_task.state = task_states[user_task.state]

    return [user_task for user_task in user_tasks]

@task_router.get('/{task_id}', response_model=TaskResponseModel)
async def get_task(task_id: int,
                     user: User = Depends(get_current_user)):

    user_task = Task.select().where(Task.id == task_id).first()

    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    if user_task.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Task is different')

    return TaskResponseModel(
        id=user_task.id,
        title=user_task.title,
        description=user_task.description,
        end_date=user_task.end_date,
        state=task_states[user_task.state],
        created_at=user_task.created_at,
        user=user.serialize()
    )


@task_router.put('/{task_id}', response_model=TaskResponseModel)
async def update_task(task_id: int,
                        task_request: TaskRequestPutModel,
                        user: User = Depends(get_current_user),
                        description = state_decription):

    user_task = Task.select().where(Task.id == task_id).first()

    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    if user_task.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Task is different')

    if task_request.title:
        user_task.title = task_request.title

    if task_request.description:
        user_task.description = task_request.description

    if task_request.end_date:
        user_task.end_date = task_request.end_date
    try:
        state = task_states[task_request.state]
        user_task.state = state
    except:
        raise HTTPException(status_code=404, detail='Code State Not found')

    user_task.save()

    return TaskResponseModel(
        id=user_task.id,
        title=user_task.title,
        description=user_task.description,
        end_date=user_task.end_date,
        state=task_states[user_task.state],
        created_at=user_task.created_at,
        user=user.serialize()
    )

@task_router.put('/states/{task_id}', response_model=TaskResponseModel)
async def update_task_state(task_id: int,
                        task_request: TaskRequestPutStateModel,
                        user: User = Depends(get_current_user),
                        description = state_decription):
    try:
        state = list(task_states.values()).index(task_request.state)
    except:
        state = None
    if not state:
        raise HTTPException(status_code=404, detail='State Name Not found')

    user_task = Task.select().where(Task.id == task_id).first()
    user_task.state = state
    user_task.save()

    return TaskResponseModel(
        id=user_task.id,
        title=user_task.title,
        description=user_task.description,
        end_date=user_task.end_date,
        state=task_states[user_task.state],
        created_at=user_task.created_at,
        user=user.serialize()
    )

@task_router.delete('/{task_id}', response_model=TaskResponseModel)
async def delete_task(task_id: int,
                        user: User = Depends(get_current_user)):

    user_task = Task.select().where(Task.id == task_id).first()

    if user_task is None:
        raise HTTPException(status_code=404, detail='Task Not found')

    if user_task.user_id != user.id:
        raise HTTPException(status_code=401, detail='Owner Task is different')

    user_task.delete_instance()

    return TaskResponseModel(
        id=user_task.id,
        title=user_task.title,
        description=user_task.description,
        end_date=user_task.end_date,
        state=task_states[user_task.state],
        created_at=user_task.created_at,
        user=user.serialize()
    )