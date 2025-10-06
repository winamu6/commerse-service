import json
from redis.asyncio import Redis
from typing import Any, Optional

class ProductCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, expire: int = 60):
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def delete_pattern(self, pattern: str):
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)