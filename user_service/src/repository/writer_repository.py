from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from user_service.src.models.user import User
from typing import Optional

class UserWriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: int, update_data: dict) -> Optional[User]:
        user = await self.session.get(User, user_id)
        if not user:
            return None

        for key, value in update_data.items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        user = await self.session.get(User, user_id)
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True

    async def update_password(self, user_id: int, new_hashed_password: str) -> bool:
        user = await self.session.get(User, user_id)
        if not user:
            return False

        user.hashed_password = new_hashed_password
        await self.session.commit()
        await self.session.refresh(user)
        return True

    async def reset_password(self, user_id: int, new_hashed_password: str) -> bool:
        return await self.update_password(user_id, new_hashed_password)