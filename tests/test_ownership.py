import pytest

@pytest.fixture
def user_a(client):
    credentials = {
        "email": "usera@example.com",
        "password": "UserAPassword123",
    }

    register_response = client.post(
        "/users/register",
        json=credentials,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json=credentials,
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "id": register_response.json()["id"],
        "email": credentials["email"],
        "headers": {
            "Authorization": f"Bearer {token}"
        },
    }

@pytest.fixture
def user_b(client):
    credentials = {
        "email": "userb@example.com",
        "password": "UserBPassword123",
    }

    register_response = client.post(
        "/users/register",
        json=credentials,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/login",
        json=credentials,
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "id": register_response.json()["id"],
        "email": credentials["email"],
        "headers": {
            "Authorization": f"Bearer {token}"
        },
    }


@pytest.fixture
def user_a_task(client, user_a):
    response = client.post(
        "/tasks",
        headers=user_a["headers"],
        json={
            "title": "User A private task",
            "description": "User B must never access this task",
            "completed": False,
        },
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def user_b_task(client, user_b):
    response = client.post(
        "/tasks",
        headers=user_b["headers"],
        json={
            "title": "User B private task",
            "description": "User A must never access this task",
            "completed": False,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_user_b_sees_only_own_tasks(
    client,
    user_a_task,
    user_b,
    user_b_task,
):
    response = client.get(
        "/tasks",
        headers=user_b["headers"],
    )

    assert response.status_code == 200

    tasks = response.json()

    task_ids = [task["id"] for task in tasks]

    assert user_b_task["id"] in task_ids
    assert user_a_task["id"] not in task_ids


def test_user_b_cannot_get_user_a_task(
    client,
    user_a_task,
    user_b,
):
    response = client.get(
        f"/tasks/{user_a_task['id']}",
        headers=user_b["headers"],
    )

    assert response.status_code == 404

def test_user_b_cannot_patch_user_a_task(
    client,
    user_a_task,
    user_b,
):
    response = client.patch(
        f"/tasks/{user_a_task['id']}",
        headers=user_b["headers"],
        json={
            "title": "Hacked by User B",
            "description": "User B changed this",
            "completed": True,
        },
    )

    assert response.status_code == 404


def test_user_b_cannot_change_user_a_task_completion(
    client,
    user_a_task,
    user_b,
):
    response = client.patch(
        f"/tasks/{user_a_task['id']}",
        headers=user_b["headers"],
        json={
            "completed": True,
        },
    )

    assert response.status_code == 404


def test_user_b_cannot_delete_user_a_task(
    client,
    user_a_task,
    user_b,
):
    response = client.delete(
        f"/tasks/{user_a_task['id']}",
        headers=user_b["headers"],
    )

    assert response.status_code == 404


def test_user_a_task_remains_unchanged_after_user_b_attack(
    client,
    user_a,
    user_a_task,
    user_b,
):
    task_id = user_a_task["id"]

    patch_response = client.patch(
        f"/tasks/{task_id}",
        headers=user_b["headers"],
        json={
            "title": "Hacked",
            "description": "Compromised",
            "completed": True,
        },
    )

    assert patch_response.status_code == 404

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=user_b["headers"],
    )

    assert delete_response.status_code == 404

    response = client.get(
        f"/tasks/{task_id}",
        headers=user_a["headers"],
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "User A private task"
    assert data["description"] == "User B must never access this task"
    assert data["completed"] is False


def test_user_a_cannot_get_user_b_task(
    client,
    user_a,
    user_b_task,
):
    response = client.get(
        f"/tasks/{user_b_task['id']}",
        headers=user_a["headers"],
    )

    assert response.status_code == 404


def test_user_a_sees_only_own_tasks(
    client,
    user_a,
    user_a_task,
    user_b_task,
):
    response = client.get(
        "/tasks",
        headers=user_a["headers"],
    )

    assert response.status_code == 200

    tasks = response.json()

    task_ids = [task["id"] for task in tasks]

    assert user_a_task["id"] in task_ids
    assert user_b_task["id"] not in task_ids


def test_new_task_is_visible_only_to_creator(
    client,
    user_a,
    user_b,
):
    create_response = client.post(
        "/tasks",
        headers=user_a["headers"],
        json={
            "title": "Automatically owned by A",
            "description": "Created while authenticated as A",
            "completed": False,
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    user_a_response = client.get(
        f"/tasks/{task_id}",
        headers=user_a["headers"],
    )

    assert user_a_response.status_code == 200

    user_b_response = client.get(
        f"/tasks/{task_id}",
        headers=user_b["headers"],
    )

    assert user_b_response.status_code == 404


