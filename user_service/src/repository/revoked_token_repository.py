import time
from redis.asyncio import Redis

class RevokedTokenRepository:
    def __init__(self, redis: Redis, prefix: str = "blacklist:"):
        self.redis = redis
        self.prefix = prefix

    async def add(self, token: str, ttl: int = None):
        key = f"{self.prefix}{token}"
        if ttl is None:
            ttl = 24 * 60 * 60
        await self.redis.setex(key, ttl, "1")

    async def is_revoked(self, token: str) -> bool:
        key = f"{self.prefix}{token}"
        exists = await self.redis.exists(key)
        return exists == 1

    async def remove(self, token: str):
        key = f"{self.prefix}{token}"
        await self.redis.delete(key)
