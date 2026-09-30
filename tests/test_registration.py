def test_register_valid_user(client):
    response = client.post(
        "/users/register",
        json={
            "email": "testusera@example.com",
            "password": "TestUserAPassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == "testusera@example.com"

    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    user_data = {
        "email": "testusera@example.com",
        "password": "TestUserAPassword123",
    }

    first_response = client.post(
        "/users/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/users/register",
        json=user_data,
    )

    assert second_response.status_code == 409


def test_register_invalid_email(client):
    response = client.post(
        "/users/register",
        json={
            "email": "this-is-not-an-email",
            "password": "TestUserAPassword123",
        },
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post(
        "/users/register",
        json={
            "email": "shortpassword@example.com",
            "password": "123",
        },
    )

    assert response.status_code == 422


def test_register_missing_email(client):
    response = client.post(
        "/users/register",
        json={
            "password": "TestUserAPassword123",
        },
    )

    assert response.status_code == 422


def test_register_missing_password(client):
    response = client.post(
        "/users/register",
        json={
            "email": "missingpassword@example.com",
        },
    )

    assert response.status_code == 422

    