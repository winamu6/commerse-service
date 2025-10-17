from user_service.src.services.writer_service import UserWriter
from user_service.src.schemas import UserUpdate
from user_service.src.services.cache_service import UserCache


class CachedUserWriter:

    def __init__(self, writer: UserWriter, cache: UserCache):
        self.writer = writer
        self.cache = cache

    async def cached_update_user(self, user_id: int, data: UserUpdate):
        updated_user = await self.writer.update_user(user_id, data)
        if updated_user:
            await self.cache.delete(f"user:{user_id}", f"user:email:{updated_user.email}")
        return updated_user

    async def cached_update_user_role(self, user_id: int, role: str):
        updated_user = await self.writer.update_user_role(user_id, role)
        if updated_user:
            await self.cache.delete(f"user:{user_id}", f"user:email:{updated_user.email}")
        return updated_user

    async def cached_delete_user(self, user_id: int):
        result = await self.writer.delete_user(user_id)
        if result:
            await self.cache.delete(f"user:{user_id}")
        return result

    async def cached_update_password(self, user_id: int, old_password: str, new_password: str):
        result = await self.writer.update_password(user_id, old_password, new_password)
        if result:
            user = await self.writer.reader.get_user_by_id(user_id)
            if user:
                await self.cache.delete(f"user:{user_id}", f"user:email:{user.email}")
        return result

    async def cached_reset_password(self, user_id: int, new_password: str):
        result = await self.writer.reset_password(user_id, new_password)
        if result:
            user = await self.writer.reader.get_user_by_id(user_id)
            if user:
                await self.cache.delete(f"user:{user_id}", f"user:email:{user.email}")
        return result