from sqlalchemy.orm import Session

from backend import models, schemas

from backend.security import (
    hash_password,
    verify_password,
)


def get_tasks(db: Session, user_id: int):
    return (db.query(models.Task).filter(models.Task.user_id == user_id).all())


def get_task(
    db: Session,
    task_id: int,
    user_id: int
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.id == task_id,
            models.Task.user_id == user_id
        )
        .first()
    )


def create_task(
    db: Session,
    task: schemas.TaskCreate,
    user_id: int
):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_task(db: Session, task_id: int, updated_task: schemas.TaskUpdate, user_id: int):
    task = get_task(
        db,
        task_id,
        user_id
    )

    if task is None:
        return None

    update_data = updated_task.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task_id: int,
    user_id: int
):
    task = get_task(
        db,
        task_id,
        user_id
    )

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return task

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )


def create_user(
    db: Session,
    user: schemas.UserCreate
):
    hashed_password = hash_password(
        user.password
    )

    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(
        db,
        email
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


def get_user_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

