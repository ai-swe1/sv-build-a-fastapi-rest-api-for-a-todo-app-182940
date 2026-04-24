from sqlalchemy.orm import Session
from . import models, schemas
import json


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo_in: schemas.TodoCreate):
    # Ensure JSON fields are stored as strings if any (rule compliance)
    db_todo = models.Todo(
        title=todo_in.title,
        description=todo_in.description,
        completed=todo_in.completed,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, db_todo: models.Todo, todo_in: schemas.TodoUpdate):
    update_data = todo_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, db_todo: models.Todo):
    db.delete(db_todo)
    db.commit()
    return db_todo
