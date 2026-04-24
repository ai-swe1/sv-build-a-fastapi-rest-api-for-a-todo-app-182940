from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crud, schemas, models, database

router = APIRouter()


@router.get("/todos", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    try:
        todos = crud.get_todos(db, skip=skip, limit=limit)
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(database.get_db)):
    try:
        todo = crud.get_todo(db, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/todos", response_model=schemas.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: schemas.TodoCreate, db: Session = Depends(database.get_db)):
    try:
        return crud.create_todo(db, todo_in)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo_in: schemas.TodoUpdate, db: Session = Depends(database.get_db)):
    try:
        db_todo = crud.get_todo(db, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return crud.update_todo(db, db_todo, todo_in)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/todos/{todo_id}", response_model=schemas.Todo)
def delete_todo(todo_id: int, db: Session = Depends(database.get_db)):
    try:
        db_todo = crud.get_todo(db, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return crud.delete_todo(db, db_todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
