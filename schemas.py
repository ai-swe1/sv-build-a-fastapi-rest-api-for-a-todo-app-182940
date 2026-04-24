from pydantic import BaseModel, Field
from datetime import datetime

class TodoSchema(BaseModel):
    id: int = Field(..., ge=0)
    title: str = Field(..., max_length=200)
    description: str | None = Field(None, max_length=1000)
    completed: bool = Field(False)
    created_at: datetime
    updated_at: datetime