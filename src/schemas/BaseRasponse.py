from pydantic import BaseModel


# схема вывода сообщений с кодом 200
class BaseResponse(BaseModel):
    status: str
    message: str
    user: dict


class TaskBaseResponse(BaseModel):
    status: str
    message: str
