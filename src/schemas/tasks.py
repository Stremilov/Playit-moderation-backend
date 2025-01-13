import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class StatusEnum(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class TaskCreateSchema(BaseModel):
    user_id: int
    description: int
    status: StatusEnum


class TaskUpdateSchema(BaseModel):
    user_id: Optional[int]
    description: Optional[int]
    status: Optional[StatusEnum]


class TaskSchema(BaseModel):
    id: int
    user_id: int
    description: str
    status: StatusEnum
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
