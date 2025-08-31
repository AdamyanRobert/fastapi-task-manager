from uuid import UUID
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Cook lunch",
                "description": "Peel the potatoes and brew tea"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task",
                "description": "Peel the potatoes and brew tea",
                "status": "in_progress"
            }
        }


class TaskResponse(BaseModel):
    """Schema for task response"""
    id: UUID
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(..., description="Task status")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Cook lunch",
                "description": "Peel the potatoes and brew tea",
                "status": "created"
            }
        }
