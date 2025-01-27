from fastapi import APIRouter, Depends, UploadFile, File, Form

from sqlalchemy.orm import Session

from api.responses import base_bad_response_for_endpoints_of_task
from core.auth import get_current_moderator_user
from schemas.BaseRasponse import TaskBaseResponse
from schemas.tasks import TaskRead, TaskListRead
from src.core.db import get_db_session
from src.services.tasks import TaskService


router = APIRouter(
    prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_moderator_user)]
)


@router.post(
    "/create",
    response_model=TaskRead,
    status_code=201,
    summary="Создание новой задачи",
    description="""
                Эндпоинт для создания задачи. Сохраняет фото в локальной папке и записывает задачу в базу данных.
                """,
    responses=base_bad_response_for_endpoints_of_task,
)
async def create_task(
    description: str = Form(...),
    value: int = Form(...),
    uploaded_file: UploadFile = File(...),
    user=Depends(get_current_moderator_user),
    session: Session = Depends(get_db_session),
):

    return await TaskService.create_tasks(
        user_id=user.id,
        description=description,
        uploaded_file=uploaded_file,
        value=value,
        session=session,
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


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskBaseResponse,
    summary="Обновления статуса задачи по id",
    responses=base_bad_response_for_endpoints_of_task,
)
async def update_task_status(
    task_id: int,
    status: str,
    session: Session = Depends(get_db_session),
):
    return await TaskService.update_task(task_id, status, session)


@router.delete(
    "/tasks/{task_id}",
    response_model=TaskBaseResponse,
    summary="Удаление задачи по id",
    responses=base_bad_response_for_endpoints_of_task,
)
async def delete_task(task_id: int, session: Session = Depends(get_db_session)):
    return await TaskService.delete_task(task_id, session)
