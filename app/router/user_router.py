from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

from fastapi.security import HTTPBasicCredentials
from fastapi import status

from ..utils.tokens import create_token

from ..schema.user_schema import UserRequestModel
from ..schema.user_schema import UserResponseModel
from ..model.users import User

users_router = APIRouter(prefix='/users')

@users_router.post('', response_model = UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El username ya existe')

    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password
    )

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