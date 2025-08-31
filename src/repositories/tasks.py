from abc import abstractmethod, ABC
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import TaskModel


class TaskRepository(ABC):
    @abstractmethod
    async def create_task(self, title, description):
        raise NotImplementedError

    @abstractmethod
    async def select_tasks(self):
        raise NotImplementedError

    @abstractmethod
    async def select_task(self, task_id):
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task_id, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task_id):
        raise NotImplementedError


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, title, description):
        task = TaskModel(
            title=title,
            description=description,
            status="created"
        )

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def select_tasks(self):
        query = select(TaskModel)
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return tasks

    async def select_task(self, task_id):
        query = select(TaskModel).where(TaskModel.id == task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return None

        return task

    async def update_task(self, task_id, **kwargs):
        query = select(TaskModel).where(TaskModel.id == task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return None

        for field, value in kwargs.items():
            if hasattr(task, field):
                setattr(task, field, value)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id):
        task = await self.select_task(task_id)

        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True

        return False
