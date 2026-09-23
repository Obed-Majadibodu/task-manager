from fastapi import FastAPI

from backend.routers import auth, tasks, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Task Manager API")

origins = ["http://127.0.0.1:5500",]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def home():
    return {"message": "Task Manager API is running"}

