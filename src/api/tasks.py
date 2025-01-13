import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Request

from src.db.db import get_db_session
from src.schemas.tasks import TaskCreateSchema
from src.utils.config import UPLOAD_FOLDER

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", summary="Создание новой задачи")
async def create_task(
    data: TaskCreateSchema,
    photo: UploadFile = File(...),
    session: Session = Depends(get_db_session),
):
    """
    Эндпоинт для создания задачи. Сохраняет фото в локальной папке и записывает задачу в базу данных.
    """
    if not photo.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    unique_filename = f"{uuid.uuid4().hex}_{photo.filename}"
    file_path = UPLOAD_FOLDER / unique_filename

    try:
        with open(file_path, "wb") as f:
            content = await photo.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save file.")

    # SQL для вставки задачи
    insert_query = text("""
        INSERT INTO tasks (description, photo_path, value, status, user_id, created_at)
        VALUES (:description, :photo_path, :value, 'pending', :user_id, NOW())
        RETURNING id, description, photo_path, value, status, created_at
    """)

    # Выполняем запрос
    try:
        result = session.execute(insert_query, {
            "description": data.description,
            "photo_path": str(file_path),
            "value": data.value,
            "user_id": data.user_id
        })
        session.commit()
        task = result.fetchone()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to create task in database.")

    # Возвращаем данные созданной задачи
    return {
        "id": task.id,
        "description": task.description,
        "photo_path": task.photo_path,
        "value": task.value,
        "status": task.status,
        "created_at": task.created_at
    }


@router.get("/", summary="Получение задач со статусом PENDING")
async def get_pending_tasks(
    request: Request,
    session: Session = Depends(get_db_session),
):
    query = text("""
        SELECT 
            id,
            description,
            photo_path,
            value,
            status,
            created_at
        FROM tasks
        WHERE status = 'pending'
        ORDER BY created_at DESC
    """)
    tasks = session.execute(query).fetchall()

    if not tasks:
        return {"tasks": []}

    formatted_tasks = []
    for task in tasks:
        photo_url = f"{UPLOAD_FOLDER}/{task.photo_path}"

        formatted_tasks.append({
            "id": task.id,
            "description": task.description,
            "photo_url": photo_url,
            "value": task.value,
            "status": task.status,
            "created_at": task.created_at,
        })

    return {"tasks": formatted_tasks}
