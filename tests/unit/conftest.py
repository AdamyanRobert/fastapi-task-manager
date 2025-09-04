import pytest
from unittest.mock import AsyncMock
import uuid
from fastapi.testclient import TestClient
from fastapi import FastAPI

from src.api.tasks import router as tasks_router
from src.models.tasks import TaskModel
from src.dependencies import get_task_service
from src.services.tasks import TaskService


@pytest.fixture
def mock_repository():
    return AsyncMock()


@pytest.fixture
def task_service(mock_repository):
    return TaskService(mock_repository)


@pytest.fixture
def app(task_service):
    test_app = FastAPI()
    test_app.include_router(tasks_router)

    test_app.dependency_overrides[get_task_service] = lambda: task_service

    return test_app


@pytest.fixture
def client(app):
    """HTTP клиент для API тестов"""
    return TestClient(app)


@pytest.fixture
def sample_task():
    return TaskModel(
        id=uuid.uuid4(),
        title="Test Task",
        description="Test Description",
        status="created"
    )


@pytest.fixture
def multiple_tasks():
    return [
        TaskModel(
            id=uuid.uuid4(),
            title="Task 1",
            description="Description 1",
            status="created"
        ),
        TaskModel(
            id=uuid.uuid4(),
            title="Task 2",
            description="Description 2",
            status="in_progress"
        ),
        TaskModel(
            id=uuid.uuid4(),
            title="Task 3",
            description="Description 3",
            status="completed"
        )
    ]
