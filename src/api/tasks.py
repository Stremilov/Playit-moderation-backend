from fastapi import APIRouter, Depends, UploadFile, File, Form

from sqlalchemy.orm import Session

from schemas.BaseRasponse import TaskBaseResponse
from schemas.tasks import TaskSchema, TaskRead, TaskListRead
from src.core.db import get_db_session
from src.services.tasks import TaskService


router = APIRouter(prefix="/tasks", tags=["Tasks"])


# TODO разделить все на сервисы и репозитории (как это сделано у юзера) - сделан
@router.post(
    "/create",
    response_model=TaskRead,
    status_code=201,
    summary="Создание новой задачи",
    description="""
                Эндпоинт для создания задачи. Сохраняет фото в локальной папке и записывает задачу в базу данных.
                """,
)
async def create_task(
    user_id: int = Form(...),
    description: str = Form(...),
    value: int = Form(...),
    uploaded_file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
):

    return await TaskService.create_tasks(
        user_id=user_id,
        description=description,
        uploaded_file=uploaded_file,
        value=value,
        session=session,
    )


@router.get(
    "/", response_model=TaskListRead, summary="Получение задач со статусом PENDING"
)
async def get_pending_tasks(session: Session = Depends(get_db_session)):
    return await TaskService.get_task_pending(session)


# TODO переписать ручку так, чтобы она при НЕ выполнении условия if status not in ["approved", "rejected"] удаляла из
#  БД таску. Тоесть если переданный статус задачи approved или rejected, то удалить ее из БД. - сделано


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskBaseResponse,
    summary="Обновления статуса задачи по id",
)
async def update_task_status(
    task_id: int, status: str, session: Session = Depends(get_db_session)
):
    return await TaskService.update_task(task_id, status, session)


@router.delete(
    "/tasks/{task_id}", response_model=TaskBaseResponse, summary="Удаление задачи по id"
)
async def delete_task(task_id: int, session: Session = Depends(get_db_session)):
    return await TaskService.delete_task(task_id, session)
