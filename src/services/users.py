from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from schemas.BaseRasponse import BaseResponse
from src.repositories.users import UserRepository


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
