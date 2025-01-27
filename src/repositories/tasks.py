from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text

from utils.Exception import NotFoundExcept, InvalidStatusExcept


class TaskRepository:
    @staticmethod
    async def create_task(
        user_id: int,
        description: str,
        photo: str,
        value: int,
        session: Session,
    ):

        # в sqlite CURRENT_TIMESTAMP в Postgresql NOW()
        insert_query = text(
            """
                    INSERT INTO tasks
                            (description,
                            photo_path, value,
                            status, user_id, created_at)
                    VALUES
                        ( :description, :photo_path,
                        :value, 'pending', :user_id,
                        CURRENT_TIMESTAMP)
                    RETURNING
                            id, description,
                            photo_path,  value,
                            status, created_at
                """
        )

        result = session.execute(
            insert_query,
            {
                "description": description,
                "photo_path": photo,
                "value": value,
                "user_id": user_id,
            },
        )
        data = result.fetchone()
        session.commit()

        return {
            "id": data.id,
            "description": data.description,
            "photo_path": data.photo_path,
            "value": data.value,
            "status": data.status,
            "created_at": data.created_at,
        }

    @staticmethod
    async def get_task_pending(session: Session):
        query = text(
            """
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
                """
        )
        tasks = session.execute(query).fetchall()

        if not tasks:
            return []

        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append(
                {
                    "id": task.id,
                    "description": task.description,
                    "photo_path": task.photo_path,
                    "value": task.value,
                    "status": task.status,
                    "created_at": task.created_at,
                }
            )

        return formatted_tasks

    @staticmethod
    async def update_task(task_id: int, status: str, session: Session):
        task = session.execute(
            text("SELECT * FROM tasks WHERE id = :task_id"), {"task_id": task_id}
        ).fetchone()

        if not task:
            raise NotFoundExcept

        if status not in ["approved", "rejected"]:
            raise InvalidStatusExcept
        else:
            session.execute(
                text("DELETE FROM tasks WHERE id = :task_id"),
                {"task_id": task_id},
            )

        session.execute(
            text("UPDATE tasks SET status = :status WHERE id = :task_id"),
            {"status": status, "task_id": task_id},
        )
        session.commit()

        return "Task status updated successfully"

    @staticmethod
    async def delete_task(task_id: int, session: Session):
        task = session.execute(
            text("SELECT * FROM tasks WHERE id = :task_id"), {"task_id": task_id}
        ).fetchone()

        if not task:
            raise NotFoundExcept

        session.execute(
            text("DELETE FROM tasks WHERE id = :task_id"), {"task_id": task_id}
        )
        session.commit()

        return "Task deleted successfully"
