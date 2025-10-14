from typing import List

from user_service.src.repository import UserReaderRepository
from user_service.src.schemas import UserRead

class UserReader:
    def __init__(self, repository: UserReaderRepository):
        self.repo = repository

    async def get_user_by_id(self, user_id: int) -> UserRead | None:
        user = await self.repo.get_user_by_id(user_id)
        return UserRead.from_orm(user) if user else None

    async def get_user_by_email(self, user_id: int) -> UserRead | None:
        user = await self.repo.get_user_by_email(user_id)
        return UserRead.from_orm(user) if user else None

    async def get_list_products(self, limit: int = 100, skip: int = 0) -> List[UserRead]:
        users = await self.repo.get_all_users(limit, skip)
        return [UserRead.from_orm(p) for p in users]