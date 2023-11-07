from pydantic import BaseModel

class UserRequestModel(BaseModel):
    username: str
    password: str


class UserResponseModel(BaseModel):
    id: int
    username: str
