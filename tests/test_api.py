import pytest
import requests


def test_create_task():
    r = requests.post(
        url="http://127.0.0.1:8000/playit/api/moderation/tasks/create",
    )
    assert r.status_code == 200


def test_get_tasks():
    r = requests.get(url="http://127.0.0.1:8000/playit/api/moderation/tasks/")
    assert r.status_code == 200


def test_update_tasks():
    r = requests.patch(
        url="http://127.0.0.1:8000/playit/api/moderation/tasks/tasks/3?status=approved"
    )
    assert r.status_code == 200


def test_del_task():
    r = requests.delete(url="http://localhost:8000/tasks/1")
    assert r.status_code == 200
