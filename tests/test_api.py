# TODO возможна надо будет сделать асинхронные тесты, тест вебсокета доделать
# TODO И зарефачить структура папок тест понять как работаю эти ебучие импорты!


def test_unauthorized_access(client):
    response = client.post("/tasks/create")
    assert response.status_code == 401


def test_create_task(client, moderator_token):
    with open("test_image.png", "rb") as f:
        response = client.post(
            "/tasks/create",
            data={"description": "Test", "value": "100"},
            files={"uploaded_file": ("test.png", f, "image/png")},
            cookies={"users_access_token": moderator_token},
        )

    assert response.status_code == 201
    assert response.json()["status"] == "success"


def test_get_pending_tasks(client, moderator_token):
    response = client.get("/tasks/", cookies={"users_access_token": moderator_token})
    assert response.status_code == 200


def test_update_task_status(client, moderator_token):
    # Создаем задачу и получаем её ID
    test_create_task(client, moderator_token)
    tasks = client.get(
        "/tasks/", cookies={"users_access_token": moderator_token}
    ).json()["task"]
    task_id = tasks[0]["id"]

    response = client.patch(
        f"/tasks/tasks/{task_id}?status=approved",
        cookies={"users_access_token": moderator_token},
    )
    assert response.status_code == 200


def test_delete_task(client, moderator_token):
    test_create_task(client, moderator_token)
    tasks = client.get(
        "/tasks/", cookies={"users_access_token": moderator_token}
    ).json()["task"]
    task_id = tasks[0]["id"]

    response = client.delete(
        f"/tasks/tasks/{task_id}", cookies={"users_access_token": moderator_token}
    )
    assert response.status_code == 200


def test_forbidden_access(client, user_token):

    response = client.get("/tasks/", cookies={"users_access_token": user_token})
    assert response.status_code == 403


def test_invalid_token(client):
    response = client.get("/tasks/", cookies={"users_access_token": "invalid_token"})
    assert response.status_code == 401
