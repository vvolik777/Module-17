from pydantic import BaseModel
from pydantic import ConfigDict


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

class TaskBase(BaseModel):
    title: str
    content: str
    priority: int
    completed: bool = False

class CreateTask(TaskBase):
    user_id: int

class UpdateTask(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    slug: str
    user_id: int

    class Config:
        from_attributes = True
