from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models.user import User
from app.models.task import Task
from app.schemas import UserResponse, CreateUser, UpdateUser, TaskResponse
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/", response_model=list[UserResponse])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create", response_model=UserResponse)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user_slug = slugify(user.username)
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=user_slug
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/update/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.query(User).filter(User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(existing_user, key, value)
    db.commit()
    db.refresh(existing_user)
    return existing_user

@router.delete("/delete/{user_id}", response_model=UserResponse)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.delete(user_to_delete)
    db.commit()
    return user_to_delete

@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks
