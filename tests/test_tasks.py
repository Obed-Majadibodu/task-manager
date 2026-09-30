def test_create_task(client, auth_headers):
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Learn pytest",
            "description": "Automate the Task Manager tests",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["title"] == "Learn pytest"
    assert data["description"] == "Automate the Task Manager tests"
    assert data["completed"] is False


def test_create_task_without_description(client, auth_headers):
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Task without description",
            "completed": False,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Task without description"
    assert data["completed"] is False


def test_create_task_without_title(client, auth_headers):
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "description": "Missing title",
            "completed": False,
        },
    )

    assert response.status_code == 422


def test_create_task_without_token(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Unauthorized task",
            "description": "This must not be created",
            "completed": False,
        },
    )

    assert response.status_code == 401

def test_get_tasks(client, auth_headers, sample_task):
    response = client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    assert data[0]["id"] == sample_task["id"]
    assert data[0]["title"] == sample_task["title"]


def test_get_task_by_id(client, auth_headers, sample_task):
    response = client.get(
        f"/tasks/{sample_task['id']}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sample_task["id"]
    assert data["title"] == "Sample task"
    assert data["description"] == "Sample task description"
    assert data["completed"] is False


def test_get_nonexistent_task(client, auth_headers):
    response = client.get(
        "/tasks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_patch_task_title(client, auth_headers, sample_task):
    response = client.patch(
        f"/tasks/{sample_task['id']}",
        headers=auth_headers,
        json={
            "title": "Patched title",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Patched title"
    assert data["description"] == "Sample task description"
    assert data["completed"] is False


def test_patch_task_completed(client, auth_headers, sample_task):
    response = client.patch(
        f"/tasks/{sample_task['id']}",
        headers=auth_headers,
        json={
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Sample task"
    assert data["description"] == "Sample task description"
    assert data["completed"] is True


def test_patch_task_with_empty_object(client, auth_headers, sample_task):
    response = client.patch(
        f"/tasks/{sample_task['id']}",
        headers=auth_headers,
        json={},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sample_task["id"]
    assert data["title"] == sample_task["title"]
    assert data["description"] == sample_task["description"]
    assert data["completed"] == sample_task["completed"]


def test_patch_nonexistent_task(client, auth_headers):
    response = client.patch(
        "/tasks/999999",
        headers=auth_headers,
        json={
            "title": "Does not exist",
        },
    )

    assert response.status_code == 404


def test_delete_task(client, auth_headers, sample_task):
    task_id = sample_task["id"]

    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Task deleted successfully"
    }

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_delete_nonexistent_task(client, auth_headers):
    response = client.delete(
        "/tasks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_patch_all_task_fields(client, auth_headers, sample_task):
    response = client.patch(
        f"/tasks/{sample_task['id']}",
        headers=auth_headers,
        json={
            "title": "Fully updated task",
            "description": "All editable fields were updated",
            "completed": True,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sample_task["id"]
    assert data["title"] == "Fully updated task"
    assert data["description"] == "All editable fields were updated"
    assert data["completed"] is True


