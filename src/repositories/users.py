from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from typing import Optional


class UserRepository:

    # TODO Переписать orm на чистый sql.
    #  Все crud операции могут быть или непосредственно в коде иди в отдельной директории crud
    @staticmethod
    async def update_user_balance(session: Session, username: str, value: int):
        statement = update(Users).where(Users.username == username).values(balance=Users.balance + value)
        session.execute(statement)
        session.commit()

        statement = select(Users).filter_by(username=username)
        result = session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return None
        return user.to_read_model()
