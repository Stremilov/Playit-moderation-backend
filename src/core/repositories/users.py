from sqlalchemy import text
from sqlalchemy.orm import Session


class UserRepository:
    @staticmethod
    async def update_user_balance(session: Session, username: str, value: int):
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

    @staticmethod
    async def get_user_by_name(username: str, session: Session):
        stmt = text("SELECT * FROM users WHERE username =:username")
        user = session.execute(stmt, {"username": username}).fetchone()
        return user

    @staticmethod
    async def create_user(username: str, role: str, session: Session):
        insert_query = text(
            """
                    INSERT INTO users
                            (username,
                            role, 
                            created_at)
                    VALUES
                        ( :username,
                          :role,
                        CURRENT_TIMESTAMP)
                """
        )
        session.execute(
            insert_query,
            {"username": username, "role": role},
        )
        session.commit()
        return "Вы успешно зарегистрированы!"
