from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from src.core.schemas.BaseRasponse import BaseResponse, TaskBaseResponse
from src.core.repositories.users import UserRepository
from src.core.utils.exceptions import handle_http_exceptions


class UserService:

    @staticmethod
    async def manage_user_balance(
        request: Request,
        session: Session,
        value: int,
        user_id: int,
    ) -> BaseResponse:
        """
        Получает значение и изменяет баланс пользователя на это значение
        """
        try:
            # TODO Сделать проверку по user_id вместо verify_user_by_jwt

            user = await UserRepository.get_user_by_id(user_id, session)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден",
                )

            user = await UserRepository.update_user_balance(
                session, user.username, value
            )

            # TODO Сделать BaseResponse
            return BaseResponse(
                status="success",
                message="Баланс пользователя успешно обновлен",
                user=user,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Произошла непредвиденная ошибка: {e}",
            )

    @staticmethod
    @handle_http_exceptions
    async def create_user(username: str, role: str, session: Session):
        msg = await UserRepository.create_user(username, role, session)
        return TaskBaseResponse(status="success", message=msg)

    @staticmethod
    @handle_http_exceptions
    async def find_user_by_name(username: str, session: Session):
        return await UserRepository.get_user_by_name(username, session)

    @staticmethod
    @handle_http_exceptions
    async def find_user_by_id(user_id: int, session: Session):
        return await UserRepository.get_user_by_id(user_id, session)
