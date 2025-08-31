from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from src.services.tasks import TaskService
from src.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_data: TaskCreate,
        service: TaskService = Depends(get_task_service)
):
    """Создать новую задачу"""
    task = await service.create_task(
        title=task_data.title,
        description=task_data.description
    )
    return task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
        service: TaskService = Depends(get_task_service)
):
    """Получить список всех задач"""
    tasks = await service.select_tasks()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    """Получить задачу по ID"""
    task = await service.select_task(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: UUID,
        task_data: TaskUpdate,
        service: TaskService = Depends(get_task_service)
):
    """Обновить задачу"""
    # Фильтруем только переданные поля
    update_data = task_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    updated_task = await service.update_task(task_id, **update_data)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: UUID,
        service: TaskService = Depends(get_task_service)
):
    deleted = await service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )