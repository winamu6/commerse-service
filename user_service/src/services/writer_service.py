from typing import Optional
from user_service.src.models import User
from user_service.src.repository import UserWriterRepository, UserReaderRepository
from user_service.src.schemas import UserRead, UserUpdate
from user_service.src.utils import get_password_hash


class UserWriter:
    def __init__(self, reader: UserReaderRepository, writer: UserWriterRepository):
        self.reader = reader
        self.writer = writer

    async def create_user(self, email: str, full_name: str, password: str) -> UserRead:
        existing = await self.reader.get_user_by_email(email)
        if existing:
            raise ValueError("email is already registered")

        hashed_password = get_password_hash(password)
        new_user = User(full_name=full_name, email=email, hashed_password=hashed_password)
        created_user = await self.writer.create_user(new_user)
        return UserRead.from_orm(created_user)

    async def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserRead]:
        update_data = data.dict(exclude_unset=True)
        updated_user = await self.writer.update_user(user_id, update_data)
        return UserRead.from_orm(updated_user) if updated_user else None

    async def delete_user(self, user_id: int) -> bool:
        return await self.writer.delete_user(user_id)