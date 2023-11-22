from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    status: Optional[str] = None


class TaskInDBBase(TaskBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
