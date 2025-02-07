from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String


class TaskModel(BaseModel):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
