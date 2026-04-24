from models import Todo
from datetime import datetime
todos = [
    Todo(title='Buy groceries', description='Buy milk, eggs, etc.', completed=False),
    Todo(title='Do laundry', description=None, completed=False)
]

def seed_database(session):
    for todo in todos:
        session.add(todo)
    session.commit()