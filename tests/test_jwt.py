from datetime import datetime, timedelta, timezone

import jwt

from backend.security import JWT_SECRET_KEY, JWT_ALGORITHM

def test_users_me_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_users_me_with_malformed_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer this-is-not-a-jwt"
        },
    )

    assert response.status_code == 401


def test_users_me_with_tampered_token(client, auth_token):
    tampered_token = auth_token[:-1] + (
        "a" if auth_token[-1] != "a" else "b"
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {tampered_token}"
        },
    )

    assert response.status_code == 401


def test_users_me_with_valid_token(client, auth_headers):
    response = client.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status_code == 200


def test_users_me_with_expired_token(client, registered_user):
    expiration = datetime.now(timezone.utc) - timedelta(minutes=1)

    expired_token = jwt.encode(
        {
            "sub": str(registered_user["id"]),
            "exp": expiration,
        },
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {expired_token}"
        },
    )

    assert response.status_code == 401

