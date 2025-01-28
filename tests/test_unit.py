# доделать все юнит тесты раз начала???
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from repositories.tasks import TaskRepository
from schemas.BaseRasponse import TaskBaseResponse
from schemas.tasks import TaskListRead
from services.tasks import TaskService


@pytest.mark.asyncio
async def test_create_task_unit_service():
    pass


@pytest.mark.asyncio
async def test_get_tasks_unit_service():
    with patch(
        "src.repositories.tasks.TaskRepository.get_task_pending",
        new_callable=AsyncMock,
    ) as mock_get_task_pending:
        mock_task = MagicMock(
            id=2,
            description="test",
            photo_path="uploads\\images\\2cacc5ae4d454332bc911604b4aebbbe_Screenshot_2.png",
            value=10,
            status="pending",
            created_at="2025-01-27T21:22:46",
        )
        mock_get_task_pending.return_value = [mock_task]

        result = await TaskService.get_task_pending(session=MagicMock(spec=Session))
        assert isinstance(result, TaskListRead)
        assert result.status == "success"
        assert result.message == "Все задачи со статусом PENDING"
        assert len(result.task) == 1
        assert result.task[0].id == 2
        assert result.task[0].description == "test"
        assert (
            result.task[0].photo_path
            == "uploads\\images\\2cacc5ae4d454332bc911604b4aebbbe_Screenshot_2.png"
        )
        mock_get_task_pending.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_task_unit_service():
    with patch(
        "src.repositories.tasks.TaskRepository.update_task",
        new_callable=AsyncMock,
    ) as mock_update_task:
        mock_update_task.return_value = "Task status updated successfully"

        result = await TaskService.update_task(
            task_id=2, status="approved", session=MagicMock(spec=Session)
        )

        assert isinstance(result, TaskBaseResponse)
        assert result.status == "success"
        assert result.message == "Task status updated successfully"
        mock_update_task.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_task_unit_service():
    with patch(
        "src.repositories.tasks.TaskRepository.delete_task",
        new_callable=AsyncMock,
    ) as mock_delete_task:
        mock_delete_task.return_value = "Task deleted successfully"
        result = await TaskService.delete_task(
            task_id=2, session=MagicMock(spec=Session)
        )
        assert isinstance(result, TaskBaseResponse)
        assert result.status == "success"
        assert result.message == "Task deleted successfully"
        mock_delete_task.assert_awaited_once()


#
# @pytest.mark.asyncio
# async def test_create_task_unit_repository():
#
@pytest.mark.asyncio
async def test_get_task_unit_repository():
    mock_session = MagicMock(spec=Session)
    mock_task = MagicMock(
        id=2,
        description="test",
        photo_path="uploads\\images\\2cacc5ae4d454332bc911604b4aebbbe_Screenshot_2.png",
        value=10,
        status="pending",
        created_at="2025-01-27T21:22:46",
    )

    mock_session.execute.return_value.fetchall.return_value = [mock_task]

    # Вызываем метод репозитория
    tasks = await TaskRepository.get_task_pending(session=mock_session)

    assert tasks == [
        {
            "id": 2,
            "description": "test",
            "photo_path": "uploads\\images\\2cacc5ae4d454332bc911604b4aebbbe_Screenshot_2.png",
            "value": 10,
            "status": "pending",
            "created_at": "2025-01-27T21:22:46",
        }
    ]
    # Проверяем, что execute был вызван
    mock_session.execute.assert_called_once()


# @pytest.mark.asyncio
# async def test_update_task_unit_repository():
#
#
# @pytest.mark.asyncio
# async def test_delete_task_unit_repository():
