import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from schemas.BaseRasponse import TaskBaseResponse


class StatusEnum(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class TaskCreateSchema(BaseModel):
    user_id: int
    description: str
    value: int


class TaskUpdateSchema(BaseModel):
    user_id: Optional[int]
    description: Optional[int]
    status: Optional[StatusEnum]


class TaskSchema(BaseModel):
    id: int
    description: str
    photo_path: str
    value: int
    status: StatusEnum
    created_at: datetime

    class Config:
        from_attributes = True


class TaskRead(TaskBaseResponse):
    task: TaskSchema


class TaskListRead(TaskBaseResponse):
    task: List[TaskSchema]
