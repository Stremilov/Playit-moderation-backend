import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database configuration for connection
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = "sqlite:///core.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


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
