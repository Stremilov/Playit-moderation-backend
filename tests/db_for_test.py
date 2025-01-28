import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from core.db import get_db_session
from main import app

"""
Создание Тестовой БД с тестовыми таблицами для интеграционных тестов АПИШКИ
"""
# TODO ЭТУ БД и тесты сделать асинхронными!
TEST_DATABASE_URL = "sqlite:///tests.db"
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=test_engine)


def init_test_db():
    with test_engine.begin() as conn:
        logging.info("Создаю таблицы!")
        stmt = text(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,             
                user_id INTEGER NOT NULL, 
                description TEXT NOT NULL,          
                photo_path VARCHAR(255) NOT NULL,   
                value INTEGER NOT NULL,                 
                status VARCHAR(50) NOT NULL DEFAULT 'pending', 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            );
        """
        )
        conn.execute(stmt)
        # create table users
        stmt = text(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,             
                username TEXT NOT NULL,             
                role VARCHAR(50) NOT NULL DEFAULT 'USER', 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
            );
        """
        )
        conn.execute(stmt)
        logging.info("Таблицы созданы!")


def init_test_users():
    with test_engine.begin() as conn:
        logging.info("Создаю тестовые юзеры!")
        stmt = text(
            """
                INSERT INTO users
                            (username,
                            role, 
                            created_at)
                    VALUES
                        ("URA",
                          "MODERATOR",
                        CURRENT_TIMESTAMP)
                """
        )
        conn.execute(stmt)
        stmt = text(
            """
                    INSERT INTO users
                            (username,
                            role, 
                            created_at)
                    VALUES
                        ( "SASHA",
                          "USER",
                        CURRENT_TIMESTAMP)
                """
        )
        conn.execute(stmt)
        logging.info("Тестовые юзеры созданы!")


def drop_all_table():
    with test_engine.begin() as conn:
        logging.info("Удаляю тестовые таблицы!")
        stmt = text(
            """
            DROP TABLE IF EXISTS users;
        """
        )
        conn.execute(stmt)
        stmt = text(
            """
            DROP TABLE IF EXISTS tasks;
        """
        )
        conn.execute(stmt)
        logging.info("Тестовые таблицы удалены!")


def override_get_db() -> TestingSessionLocal:
    try:
        session: Session = TestingSessionLocal()
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db_session] = override_get_db
