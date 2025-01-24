from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from src.api.responses import (
    update_user_balance_responses
)
from src.db.db import get_db_session
from src.services.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.put(
    path="/{user_id}/balance/{value}",
    response_model=BaseResponse,
    summary="Изменение баланса пользователя",
    description="""
    Изменяет баланс пользователю (как в положительную так и отрицательную сторону) и возвращает всего пользователя

    - Проверяет наличие токена в куки, если его не будет, то вернёт 401 HTTP status_code;
    - Декодирует и проверяет JWT-токен, если он некорректен, то вернёт 401 HTTP status_code;
    - Ищет пользователя по username из JWT-токена в базе данных, если не находит, то возвращает 404 HTTP status_code;
    - Изменяет баланс пользователя как в положительную так и отрицательную сторону (нужно передать или 100 или -100 к примеру)
    - Возвращает все данные пользователя
    """,
    responses=update_user_balance_responses
)
async def manage_balance(
        user_id: int,
        value: int,
        request: Request,
        session: Session = Depends(get_db_session),
):
    return await UserService.manage_user_balance(request=request, session=session, value=value, user_id=user_id)