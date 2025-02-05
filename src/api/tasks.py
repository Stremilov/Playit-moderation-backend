from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from src.api.responses import base_bad_response_for_endpoints_of_task
from src.core.schemas.tasks import TaskListRead
from src.core.database.db import get_db_session
from src.core.services.tasks import TaskService

router = APIRouter(
    prefix="/tasks", tags=["Tasks"]
)


@router.get(
    "/",
    response_model=TaskListRead,
    summary="Получение задач со статусом PENDING",
    description="""
        -Получение списка задач со статусом PENDING только для авторизованных пользователей с ролью МОДЕРАТОР
        """,
    responses=base_bad_response_for_endpoints_of_task,
)
async def get_pending_tasks(session: Session = Depends(get_db_session)):
    return await TaskService.get_task_pending(session)



