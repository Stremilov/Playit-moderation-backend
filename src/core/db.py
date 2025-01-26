from sqlalchemy import (
    create_engine,
    text,
)
from sqlalchemy.orm import sessionmaker
import logging

# Database configuration for connection
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = "sqlite:///core.core"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


"""
Создаю регистрацию чисто для аутентификации по JWT po cookies on fastapi_users
1.сделать модель
2.сделать готового UserManager
3.иницилизировать CookieTransport
4.сделать функцию зависимость get_jwt_strategy
5.auth_backend
6. initial Fastapi_Users
"""


def initDB():
    with engine.begin() as conn:
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
        logging.info("Таблицы созданы!")
