from typing import Optional
from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
