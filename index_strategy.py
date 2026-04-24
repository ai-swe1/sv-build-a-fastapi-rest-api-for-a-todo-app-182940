from sqlalchemy import Index
from models import Todo
Index('ix_todos_title', Todo.title)