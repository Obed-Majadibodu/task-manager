from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud, schemas
from backend.auth import get_current_user
from backend.database import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Get all the tasks
@router.get(
    "",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_tasks(
        db,
        current_user.id
    )

# Create a task
@router.post(
    "",
    response_model=schemas.TaskResponse,
    status_code=201
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_task(
        db,
        task,
        current_user.id
    )

# Get a single task
@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = crud.get_task(
        db,
        task_id,
        current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

# Update a task
@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse
)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = crud.update_task(
        db,
        task_id,
        updated_task,
        current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

# Delete a task
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = crud.delete_task(
        db,
        task_id,
        current_user.id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }

