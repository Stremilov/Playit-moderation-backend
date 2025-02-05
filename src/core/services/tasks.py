from sqlalchemy.orm import Session

from src.core.schemas.tasks import TaskListRead
from src.core.repositories.tasks import TaskRepository
from src.core.utils.exceptions import handle_http_exceptions


class TaskService:

    @staticmethod
    @handle_http_exceptions
    async def get_task_pending(session: Session):
        list_task = await TaskRepository.get_task_pending(session=session)
        return TaskListRead(
            status="success", message="Все задачи со статусом PENDING", task=list_task
        )
