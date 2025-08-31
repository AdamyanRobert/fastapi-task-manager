from src.repositories.tasks import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    async def select_tasks(self):
        return await self.repository.select_tasks()

    async def select_task(self, task_id):
        return await self.repository.select_task(task_id)

    async def create_task(self, title, description):
        return await self.repository.create_task(title, description)

    async def update_task(self, task_id, **kwargs):
        return await self.repository.update_task(task_id, **kwargs)

    async def delete_task(self, task_id):
        return await self.repository.delete_task(task_id)
