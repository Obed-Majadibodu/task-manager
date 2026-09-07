from sqlalchemy.orm import Session

from backend import models, schemas


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int):
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )


def create_task(db: Session, task: schemas.TaskCreate):
    new_task = models.Task(
        title=task.title,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def update_task(
    db: Session,
    task_id: int,
    updated_task: schemas.TaskUpdate
):
    task = get_task(db, task_id)

    if task is None:
        return None

    if updated_task.title is not None:
        task.title = updated_task.title

    if updated_task.completed is not None:
        task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return task