from redis.asyncio import Redis
from payment_service.src.db.settings import settings
from payment_service.src.services.cache_service import PaymentCache

redis_client = Redis.from_url(
    settings.REDIS_URL,
    encoding="UTF-8",
    decode_responses=True,
)

cache_service = PaymentCache(redis_client)