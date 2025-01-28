from fastapi import UploadFile
from sqlalchemy.orm import Session

from schemas.BaseRasponse import TaskBaseResponse
from schemas.tasks import TaskListRead, TaskRead
from src.repositories.tasks import TaskRepository
from utils.Exception import handle_http_exceptions
from utils.uploaded_file import upload_file


class TaskService:
    @staticmethod
    @handle_http_exceptions
    async def create_tasks(
        user_id: int,
        description: str,
        uploaded_file: UploadFile,
        value: int,
        session: Session,
    ):
        photo = await upload_file(uploaded_file)
        new_task = await TaskRepository.create_task(
            user_id, description, photo, value, session
        )
        return TaskRead(status="success", message="Создана новая Задача", task=new_task)

    @staticmethod
    @handle_http_exceptions
    async def get_task_pending(session: Session):
        list_task = await TaskRepository.get_task_pending(session=session)
        return TaskListRead(
            status="success", message="Все задачи со статусом PENDING", task=list_task
        )

    @staticmethod
    @handle_http_exceptions
    async def update_task(task_id: int, status: str, session: Session):

        msg = await TaskRepository.update_task(task_id, status, session)
        return TaskBaseResponse(status="success", message=msg)

    @staticmethod
    @handle_http_exceptions
    async def delete_task(task_id: int, session: Session):
        msg = await TaskRepository.delete_task(task_id, session)
        return TaskBaseResponse(status="success", message=msg)
