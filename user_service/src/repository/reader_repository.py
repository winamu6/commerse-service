from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional, List

from user_service.src.models import User
from user_service.src.utils import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, full_name: str, email: str, password: str, password_confirm: str) -> User:
        if password == password_confirm:
            hashed_password = hash_password(password)
            user = User(full_name = full_name, email=email, hashed_password=hashed_password)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Task]:
        stmt = select(Task)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        return await self.session.get(Task, task_id)

    async def get_by_date_range(self, start_date: Date, end_date: Date) -> User:
        stmt = (
            select(User)
            .where(and_(Task.date >= start_date, Task.date <= end_date))
            .order_by(Task.date.asc())
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def update(self, task_id: int, date: Date = None, description: str = None, cost: int = None) -> Optional[Task]:
        task = await self.session.get(Task, task_id)
        if not task:
            return None
        if date:
            task.date = date
        if description:
            task.description = description
        if cost:
            task.cost = cost
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: int) -> bool:
        task = await self.session.get(Task, task_id)
        if not task:
            return False
        await self.session.delete(task)
        await self.session.commit()
        return True