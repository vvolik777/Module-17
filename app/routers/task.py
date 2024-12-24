from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import TaskResponse, CreateTask, UpdateTask
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/", response_model=list[TaskResponse])
async def all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task

@router.post("/create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: CreateTask, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == task.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    task_slug = slugify(task.title)
    new_task = Task(
        title=task.title,
        content=task.content,
        priority=task.priority,
        completed=task.completed,
        slug=task_slug,
        user_id=task.user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/update/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(existing_task, key, value)
    db.commit()
    db.refresh(existing_task)
    return existing_task

@router.delete("/delete/{task_id}", response_model=TaskResponse)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_to_delete = db.query(Task).filter(Task.id == task_id).first()
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    db.delete(task_to_delete)
    db.commit()
    return task_to_delete
