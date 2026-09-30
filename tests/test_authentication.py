def test_login_with_correct_credentials(client, registered_user):
    response = client.post(
        "/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client, registered_user):
    response = client.post(
        "/login",
        json={
            "email": registered_user["email"],
            "password": "DefinitelyWrongPassword123",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert "access_token" not in data


def test_login_with_nonexistent_user(client):
    response = client.post(
        "/login",
        json={
            "email": "nobody@example.com",
            "password": "SomePassword123",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert "access_token" not in data


def test_login_missing_email(client):
    response = client.post(
        "/login",
        json={
            "password": "SomePassword123",
        },
    )

    assert response.status_code == 422


def test_login_missing_password(client):
    response = client.post(
        "/login",
        json={
            "email": "testuser@example.com",
        },
    )

    assert response.status_code == 422


def test_get_current_user(client, registered_user, auth_headers):
    response = client.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["email"] == registered_user["email"]

    assert "password" not in data
    assert "hashed_password" not in data

    