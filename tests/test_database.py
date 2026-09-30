import pytest
from sqlalchemy.exc import IntegrityError

from backend import models

def test_password_is_hashed_in_database(
    client,
    registered_user,
    db_session,
):
    user = (
        db_session.query(models.User)
        .filter(models.User.id == registered_user["id"])
        .first()
    )

    assert user is not None

    assert user.hashed_password != registered_user["password"]

    assert registered_user["password"] not in user.hashed_password


def test_task_user_id_matches_owner(
    client,
    registered_user,
    auth_headers,
    sample_task,
    db_session,
):
    task = (
        db_session.query(models.Task)
        .filter(models.Task.id == sample_task["id"])
        .first()
    )

    assert task is not None

    assert task.user_id == registered_user["id"]


def test_postgresql_rejects_nonexistent_task_owner(
    client,
    db_session,
):
    invalid_task = models.Task(
        title="Invalid owner task",
        description="This user does not exist",
        completed=False,
        user_id=999999,
    )

    db_session.add(invalid_task)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()


def test_cannot_delete_user_who_still_owns_tasks(
    client,
    registered_user,
    sample_task,
    db_session,
):
    user = (
        db_session.query(models.User)
        .filter(models.User.id == registered_user["id"])
        .first()
    )

    assert user is not None

    db_session.delete(user)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()