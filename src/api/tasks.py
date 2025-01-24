import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
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


# TODO разделить все на сервисы и репозитории (как это сделано у юзера)

@router.post("/create", summary="Создание новой задачи")
async def create_task(
        request: Request,
        data: TaskCreateSchema,
        uploaded_file: UploadFile,
        session: Session = Depends(get_db_session),
):
    """
    Эндпоинт для создания задачи. Сохраняет фото в локальной папке и записывает задачу в базу данных.
    """
    unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.filename}"
    file_path = UPLOAD_FOLDER / unique_filename

    try:
        with open(file_path, "wb") as f:
            content = await uploaded_file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)

    insert_query = text("""
        INSERT INTO tasks (description, photo_path, value, status, user_id, created_at)
        VALUES (:description, :photo_path, :value, 'pending', :user_id, NOW())
        RETURNING id, description, photo_path, value, status, created_at
    """)

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to create task in database.")

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


# TODO переписать ручку так, чтобы она при НЕ выполнении условия if status not in ["approved", "rejected"] удаляла из
#  БД таску. Тоесть если переданный статус задачи approved или rejected, то удалить ее из БД.

@router.patch("/tasks/{task_id}")
async def update_task_status(
        task_id: int,
        status: str,
        session: Session = Depends(get_db_session)
):
    task = session.execute(
        text("SELECT * FROM tasks WHERE id = :task_id"),
        {"task_id": task_id}
    ).fetchone()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    session.execute(
        text("UPDATE tasks SET status = :status WHERE id = :task_id"),
        {"status": status, "task_id": task_id}
    )
    session.commit()


    return {"message": "сююю"}
