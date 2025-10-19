import json
from typing import Optional
from src.services.reader_service import UserReader
from src.schemas import UserRead
from src.services.cache_service import UserCache


class CachedUserReader:

    def __init__(self, reader: UserReader, cache: UserCache):
        self.reader = reader
        self.cache = cache

    async def get_cached_user_by_id(self, user_id: int) -> Optional[UserRead]:
        cache_key = f"user:{user_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return UserRead(**cached)

        user = await self.reader.get_user_by_id(user_id)
        if user:
            await self.cache.set(cache_key, user.dict(), expire=120)
        return user

    async def get_cached_user_by_mail(self, mail: str) -> Optional[UserRead]:
        cache_key = f"user:email:{mail}"
        cached = await self.cache.get(cache_key)
        if cached:
            return UserRead(**cached)

        user = await self.reader.get_user_by_mail(mail)
        if user:
            await self.cache.set(cache_key, user.dict(), expire=120)
        return user

    async def get_cached_all_users(self, limit: int = 100, skip: int = 0):
        cache_key = f"users:list:{skip}:{limit}"
        cached = await self.cache.get(cache_key)
        if cached:
            users = [UserRead.parse_raw(u) for u in json.loads(cached)]
            return users

        users = await super().get_all_users(limit, skip)
        await self.cache.set(cache_key, json.dumps([u.json() for u in users]), ex=300)
        return users