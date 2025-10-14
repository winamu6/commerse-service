from user_service.src.services.writer_service import UserWriter
from user_service.src.schemas import UserRead, UserUpdate
from user_service.src.services.cache_service import UserCache


class CachedUserWriter:

    def __init__(self, writer: UserWriter, cache: UserCache):
        self.writer = writer
        self.cache = cache

    async def update_user(self, user_id: int, data: UserUpdate):
        updated_user = await self.writer.update_user(user_id, data)
        if updated_user:
            await self.cache.delete(f"user:{user_id}", f"user:email:{updated_user.email}")
        return updated_user

    async def delete_user(self, user_id: int):
        result = await self.writer.delete_user(user_id)
        if result:
            await self.cache.delete(f"user:{user_id}")
        return result
