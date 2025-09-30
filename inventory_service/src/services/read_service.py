from datetime import date as Date
from typing import List

from inventory_service.src.repository import ProductRepository
from inventory_service.src.schemas import TaskRead

class TaskReader:
    def __init__(self, repository: TaskRepository):
        self.repo = repository

    async def get_all_tasks(self, limit: int = 100, offset: int = 0) -> List[TaskRead]:
        tasks = await self.repo.get_all(limit, offset)
        return [TaskRead.from_orm(t) for t in tasks]

    async def get_tasks_by_date(self, start_date: Date, end_date: Date) -> List[TaskRead]:
        tasks = await self.repo.get_by_date_range(start_date, end_date)
        return [TaskRead.from_orm(t) for t in tasks]