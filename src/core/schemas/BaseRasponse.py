import enum
from datetime import datetime

from pydantic import BaseModel


class RoleEnum(enum.Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


# схема вывода сообщений с кодом 200
class BaseResponse(BaseModel):
    status: str
    message: str
    user: dict


class TaskBaseResponse(BaseModel):
    status: str
    message: str


class UserCreateSchema(BaseModel):
    username: str
    role: RoleEnum


class UserSchema(BaseModel):
    id: int
    username: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True
