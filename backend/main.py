from fastapi import FastAPI

from backend.routers import auth, tasks, users


app = FastAPI(
    title="Task Manager API"
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "Task Manager API is running"}

