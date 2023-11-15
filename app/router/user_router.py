from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi.security import HTTPBasicCredentials
from fastapi import status

from ..utils.tokens import create_token
from ..utils.db import get_db

from ..schema.user_schema import UserRequestModel
from ..schema.user_schema import UserResponseModel
from ..model.users import User

users_router = APIRouter(prefix='/users')

@users_router.post('', response_model = UserResponseModel)
async def create_user(user: UserRequestModel,
                      db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(409, 'El username ya existe')

    hash_password = User.create_password(user.password)
    user = User(
        username = user.username,
        password = hash_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponseModel(
        id=user.id,
        username=user.username
    )


@users_router.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    if user:
        return {
            'access_token': create_token(user),
            'token_type': 'Bearer'
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Username or password incorrect',
        headers={
            'WWW-Authenticate': 'Bearer'
        }
    )