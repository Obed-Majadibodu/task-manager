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
        description=task.description,
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

    update_data = updated_task.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

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