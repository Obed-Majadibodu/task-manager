from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import SessionLocal

app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Task Manager API is running"}

@app.get(
    "/tasks",
    response_model=list[schemas.TaskResponse]
)
def get_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):

    return crud.create_task(db, task)

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    updated_task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    task = crud.update_task(
        db,
        task_id,
        updated_task
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.delete_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "message": "Task deleted successfully"
    }

