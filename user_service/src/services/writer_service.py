from typing import Optional
from src.models import User
from src.repository import UserWriterRepository, UserReaderRepository
from src.schemas import UserRead, UserUpdate, UserCreate
from src.utils import get_password_hash, verify_password


class UserWriter:
    def __init__(self, reader: UserReaderRepository, writer: UserWriterRepository):
        self.reader = reader
        self.writer = writer

    async def create_user(self, data: UserCreate) -> UserRead:
        existing = await self.reader.get_user_by_email(data.email)
        if existing:
            raise ValueError("email is already registered")

        hashed_password = get_password_hash(data.password)
        new_user = User(full_name=data.full_name, email=data.email, hashed_password=hashed_password)
        created_user = await self.writer.create_user(new_user)
        return UserRead.from_orm(created_user)

    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserRead]:
        update_data = data.dict(exclude_unset=True)
        updated_user = await self.writer.update_user(user_id, update_data)
        return UserRead.from_orm(updated_user) if updated_user else None

    async def update_user_role(self, user_id: int, role: str) -> Optional[UserRead]:
        updated_user = await self.writer.update_user_role(user_id, role)
        return UserRead.from_orm(updated_user) if updated_user else None

    async def delete_user(self, user_id: int) -> bool:
        return await self.writer.delete_user(user_id)

    async def update_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        user = await self.reader.get_user_by_id(user_id)
        if not user:
            return False

        if not verify_password(old_password, user.hashed_password):
            raise ValueError("Old password is incorrect")

        new_hashed_password = get_password_hash(new_password)
        return await self.writer.update_password(user_id, new_hashed_password)

    async def reset_password(self, user_id: int, new_password: str) -> bool:
        new_hashed_password = get_password_hash(new_password)
        return await self.writer.reset_password(user_id, new_hashed_password)