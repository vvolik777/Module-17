from fastapi import FastAPI
from app.routers import user, task

app = FastAPI()


@app.get("/")
async def Welcome():
    return {"message": "Welcome to Taskmanager"}


app.include_router(user.router)
app.include_router(task.router)
