from redis.asyncio import Redis
from cart_service.src.db.settings import settings
from cart_service.src.services.cache_service import CartCache

redis_client = Redis.from_url(
    settings.REDIS_URL,
    encoding="UTF-8",
    decode_responses=True,
)

cache_service = CartCache(redis_client)