from sqlalchemy.orm import Session
from sqlalchemy import text


class UserRepository:
    # TODO Переписать orm на чистый sql.
    #  Все crud операции могут быть или непосредственно в коде иди в отдельной директории crud - сделано
    @staticmethod
    async def update_user_balance(session: Session, username: str, value: int):
        # statement = update(Users).where(Users.username == username).values(balance=Users.balance + value)
        statement = text(
            "UPDATE users SET balance = balance + :value WHERE username = :username"
        )
        session.execute(statement, {"username": username, "value": value})
        session.commit()

        statement = text("SELECT * FROM users WHERE username = :username")
        user = session.execute(statement, {"username": username}).fetchone()

        if not user:
            return None
        return user.to_read_model()

    @staticmethod
    async def get_user_by_id(user_id: int, session: Session):
        stmt = text("SELECT * FROM users WHERE id =:user_id")
        user = session.execute(stmt, {"user_id": user_id}).fetchone()
        return user
