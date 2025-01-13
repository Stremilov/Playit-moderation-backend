from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.utils.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import logging

# Database configuration for connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
