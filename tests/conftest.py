import pytest
from fastapi.testclient import TestClient

from core.auth import create_encoded_access_token
from main import app
from tests.db_for_test import drop_all_table, init_test_db, init_test_users


@pytest.fixture(autouse=True, scope="session")
def startup_event():
    """
    Удаление и создание таблиц перед тестом
    """
    init_test_db()
    init_test_users()
    yield
    drop_all_table()


# хотел сделать отдельными фикстурами не получилось :(
@pytest.fixture(scope="session")
def setup_and_teardown():
    """
    Создание Тестовых пользователя и Модератора
    """

    yield


@pytest.fixture(scope="session")
def moderator_token():
    payload = {"sub": "1"}
    return create_encoded_access_token(payload)


@pytest.fixture(scope="session")
def user_token():
    payload = {"sub": "2"}
    return create_encoded_access_token(payload)


@pytest.fixture
def client():
    return TestClient(app=app, base_url="http://localhost:8000/playit/api/moderation")
