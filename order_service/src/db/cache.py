from redis.asyncio import Redis
from src.db.settings import settings
from src.services.cache_service import OrderCache

redis_client = Redis.from_url(
    settings.REDIS_URL,
    encoding="UTF-8",
    decode_responses=True,
)

cache_service = OrderCache(redis_client)