from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import session_async
from src.repositories.tasks import SQLAlchemyTaskRepository, TaskRepository
from src.services.tasks import TaskService


async def get_db_session() -> AsyncSession:
    async with session_async() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def get_task_repository(session: AsyncSession = Depends(get_db_session)):
    return SQLAlchemyTaskRepository(session)


async def get_task_service(repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(repository)
