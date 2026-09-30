import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app

# Import the models so SQLAlchemy knows about all tables
from backend import models

TEST_USER_EMAIL = "testuser@example.com"
TEST_USER_PASSWORD = "TestPassword123"


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL is not set. "
        "Add it to your .env file before running tests."
    )

if "task_manager_test" not in TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL must point to the task_manager_test database."
    )


test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(client):
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()
        

@pytest.fixture
def registered_user(client):
    user_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
    }

    response = client.post(
        "/users/register",
        json=user_data,
    )

    assert response.status_code == 201

    created_user = response.json()

    return {
        "id": created_user["id"],
        "email": user_data["email"],
        "password": user_data["password"],
    }

@pytest.fixture
def auth_token(client, registered_user):
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

    return data["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}"
    }


@pytest.fixture
def sample_task(client, auth_headers):
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Sample task",
            "description": "Sample task description",
            "completed": False,
        },
    )

    assert response.status_code == 201

    return response.json()

