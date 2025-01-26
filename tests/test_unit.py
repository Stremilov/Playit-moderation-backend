import sys
import os

# Добавляем корневую папку проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, AsyncMock

import pytest
from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.repositories.tasks import TaskRepository
from src.services.tasks import TaskService


@pytest.mark.asyncio
async def test_create_task_unit_service():
    mock_session = MagicMock(spec=Session)
    mock_uploaded_file = MagicMock(spec=UploadFile)
    mock_uploaded_file.filename = "test_file.png"

    # Мокируем TaskRepository.create_task
    mock_task_repo_create_task = AsyncMock(
        return_value={
            "id": 1,
            "user_id": 1,
            "description": "Test task",
            "photo_path": "uploads/test_file.png",
            "value": 100,
            "status": "pending",
        }
    )

    # Подменяем метод create_task в TaskRepository
    TaskRepository.create_task = mock_task_repo_create_task

    # Вызываем метод create_tasks
    result = await TaskService.create_tasks(
        user_id=1,
        description="Test task",
        uploaded_file=mock_uploaded_file,
        value=100,
        session=mock_session,
    )

    # Проверяем результат
    assert result == {
        "task": {
            "id": 1,
            "user_id": 1,
            "description": "Test task",
            "photo_path": "uploads/test_file.png",
            "value": 100,
            "status": "pending",
        },
        "massage": "Task create!",
    }

    # # Проверяем, что TaskRepository.create_task был вызван с правильными аргументами
    # mock_task_repo_create_task.assert_called_once_with(
    #     user_id=1,
    #     description="Test task",
    #     uploaded_file=mock_uploaded_file,
    #     value=100,
    #     session=mock_session,
    # )


@pytest.mark.asyncio
async def test_get_tasks_unit_service():
    mock_session = MagicMock(spec=Session)
    # Мокируем TaskRepository.create_task
    mock_repo_get_task_pending = AsyncMock(
        return_value={
            "tasks": {
                "id": 1,
                "user_id": 1,
                "description": "Test task",
                "photo_path": "uploads/test_file.png",
                "value": 100,
                "status": "pending",
            }
        }
    )

    # Подменяем метод create_task в TaskRepository
    TaskRepository.get_task_pending = mock_repo_get_task_pending
    result = await TaskService.get_task_pending(mock_session)
    assert len(result) == 1
    mock_repo_get_task_pending.assert_called_once_with(session=mock_session)


@pytest.mark.asyncio
async def test_update_task_unit_service():
    mock_session = MagicMock(spec=Session)
    mock_task_repo_update = AsyncMock(
        return_value={"message": "Task status updated successfully"}
    )
    # Подменяем метод create_task в TaskRepository
    TaskRepository.update_task = mock_task_repo_update
    result = await TaskService.update_task()


#
#
# @pytest.mark.asyncio
# async def test_delete_task_unit_service():
#
#
# @pytest.mark.asyncio
# async def test_create_task_unit_repository():
#
# @pytest.mark.asyncio
# async def test_get_task_unit_repository():
#
# @pytest.mark.asyncio
# async def test_update_task_unit_repository():
#
#
# @pytest.mark.asyncio
# async def test_delete_task_unit_repository():
