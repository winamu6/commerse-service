from typing import List
from src.repository import UserReaderRepository
from src.schemas import UserRead


class UserReader:
    def __init__(self, repository: UserReaderRepository):
        self.repo = repository

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        user = await self.repo.get_user_by_id(user_id)
        return UserRead.from_orm(user) if user else None

    async def get_user_by_email(self, email: str) -> UserRead | None:
        user = await self.repo.get_user_by_email(email)
        return UserRead.from_orm(user) if user else None

    async def get_all_users(self, limit: int = 100, skip: int = 0) -> List[UserRead]:
        users = await self.repo.get_all_users(skip=skip, limit=limit)
        return [UserRead.from_orm(u) for u in users]