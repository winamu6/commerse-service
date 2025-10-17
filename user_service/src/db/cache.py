from redis.asyncio import Redis
from user_service.src.db.settings import settings
from user_service.src.services.cache_service import UserCache

redis_client = Redis.from_url(
    settings.REDIS_URL,
    encoding="UTF-8",
    decode_responses=True,
)

cache_service = UserCache(redis_client)
